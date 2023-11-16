import datetime
import logging
from typing import Literal

import discord
from apscheduler.triggers.cron import CronTrigger
from discord import app_commands
from discord.ext import commands
from sqlalchemy import delete
from sqlalchemy.future import select

import app.bot
from app.cogs.utils.message_utils import join_texts
from app.cogs.utils.reminders_utils import get_remind_date
from app.config import get_guilds
from app.database.models.group_reminders import GroupReminders

logger = logging.getLogger(__name__)


class GroupReminder(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    async def send_signup_message(
        self,
        channel: discord.TextChannel | discord.Thread,
        reminder_text: str,
        author_id: int,
        remind_date: str,
    ) -> discord.Message:
        """Send a signup message to a channel to which users can react.

        Args:
            channel (discord.Channel): The channel to send the message to.
            reminder_text (str): The message to send with the reminder.
            author_id (int): The user ID of the author of the reminder.
            remind_date (str): The date of the reminder.

        Returns:
            discord.Message: The message that was sent.
        """

        message: discord.Message = await channel.send(
            join_texts(
                f"Reminder created by <@{author_id}> with message:",
                f"> {reminder_text}",
                f"You will be reminded on {remind_date} UTC.",
                "React to this message if you want to get the reminder as well!",
                separator="\n",
            ),
        )
        await message.add_reaction("✅")

        return message

    @app_commands.command(
        name="group_reminder",
        description="Set a group reminder to be sent to all users which react to a message.",
    )
    @app_commands.checks.cooldown(1, 60)
    @app_commands.guilds(*get_guilds())
    async def _group_remindme(
        self,
        interaction: discord.Interaction,
        value: app_commands.Range[int, 1, 366 * 3],
        unit: Literal["minutes", "hours", "days"],
        reminder_text: str,
    ) -> None:
        """Function which handles the /remindme command.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
            value (app_commands.Range[int, 1, 366 * 3]): The value of the reminder.
            unit (Literal["minutes", "hours", "days"]): The unit of the reminder.
            reminder_text (str): The message to send with the reminder.
            send_direct_message (bool, optional): Whether or not to send a direct message to the user. Defaults to False.
        """

        await interaction.response.defer(ephemeral=True, thinking=True)

        remind_date = get_remind_date(value, unit).replace(second=0, microsecond=0)
        signup_message = await self.send_signup_message(
            interaction.channel,  # type: ignore
            reminder_text=reminder_text,
            author_id=interaction.user.id,
            remind_date=remind_date.strftime("%Y-%m-%d %H:%M"),
        )

        reminder = GroupReminders(
            AuthorID=interaction.user.id,
            RemindDate=remind_date.strftime("%Y-%m-%d %H:%M"),
            CreationDate=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            ChannelID=interaction.channel_id,
            Message=reminder_text,
            SignupMessageID=signup_message.id,
        )

        async with self.bot.session() as session:
            session.add(reminder)
            await session.commit()

        await interaction.followup.send(f"Reminder set for {value} {unit}")

    async def check_group_reminders(self) -> None:
        """Check the database for reminders that need to be sent."""

        now = datetime.datetime.utcnow().replace(second=0, microsecond=0)

        async with self.bot.session() as session:
            query_results = (
                await session.execute(
                    select(GroupReminders).where(GroupReminders.RemindDate <= str(now))
                )
            ).fetchall()

        logger.info(f"Got {len(query_results)} reminders")
        for result in query_results:
            reminder_obj = result[0]  # Access the first (and only) element in result
            author_id = reminder_obj.AuthorID
            channel_id = reminder_obj.ChannelID
            message = reminder_obj.Message
            creation_date = reminder_obj.CreationDate
            signup_message_id = reminder_obj.SignupMessageID

            await self.respond_to_group_reminder(
                author_id=author_id,
                channel_id=channel_id,
                reminder_text=message,
                creation_date=creation_date,
                signup_message_id=signup_message_id,
            )

        async with self.bot.session() as session:
            await session.execute(
                delete(GroupReminders).where(
                    GroupReminders.ReminderID.in_([x[0].ReminderID for x in query_results])
                )
            )
            await session.commit()

    async def respond_to_group_reminder(
        self,
        author_id: int,
        channel_id: int,
        reminder_text: str,
        creation_date: str,
        signup_message_id: int,
    ) -> None:
        """Sends a reminder to channel mentioning all users which reacted to a message.

        Args:
            author_id (int): The user ID of the author of the reminder.
            channel_id (int): The channel ID to send the reminder to.
            reminder_text (str): The message provided by the user to send with the reminder.
            creation_date (str): The date of the reminder creation.
            signup_message_id (int): The message ID of the message to which the reminder is attached.
        """

        target_channel = self.bot.get_channel(channel_id)

        logger.info(
            f"Respond with remainder arguments: userid={author_id}, channelid={channel_id}, msg={reminder_text}"
        )

        if target_channel:
            target_message: discord.PartialMessage = target_channel.get_partial_message(  # type: ignore
                signup_message_id
            )

            message = await target_message.fetch()
            users_to_remind: set[int] = set()
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.bot:
                        continue
                    users_to_remind.add(user.id)

            await target_channel.send(  # type: ignore
                join_texts(
                    f"Reminder created by <@{author_id}> on {creation_date} UTC with message:",
                    f"> {reminder_text}",
                    f"||Users which reacted to the remind message: {', '.join([f'<@{user_id}>' for user_id in users_to_remind])}||",
                    separator="\n",
                )
            )

    @commands.Cog.listener("on_ready")
    async def set_scheduler(self) -> None:
        """Add the check_reminders function to the scheduler."""

        logger.info("Check group reminders added")
        self.bot.scheduler.add_job(self.check_group_reminders, CronTrigger(second=0))

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        """Handle errors for application commands.

        Args:
            interaction (discord.Interaction): The interaction that triggered the error.
            error (Exception): The error that was triggered.
        """

        logger.error(type(error), error)

        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: app.bot.Bot) -> None:
    """Add the Reminder cog to the bot.

    Args:
        bot (app.bot.Bot): the bot instance to which the cog should be added.
    """

    await bot.add_cog(GroupReminder(bot))
