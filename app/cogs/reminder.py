import datetime
import logging

import discord
from apscheduler.triggers.cron import CronTrigger
from discord import app_commands
from discord.ext import commands
from sqlalchemy import delete
from sqlalchemy.future import select

import app.bot
from app.cogs.utils.message_utils import join_texts
from app.cogs.utils.reminder_utils import InvalidReminderDate, get_date, validate_text
from app.config import get_guilds
from app.database.models.reminders import Reminders

logger = logging.getLogger(__name__)


class Reminder(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="remindme",
        description="Set a reminder",
    )
    @app_commands.checks.cooldown(1, 30)
    @app_commands.guilds(*get_guilds())
    async def _remindme(
        self,
        interaction: discord.Interaction,
        target_date: str,
        reminder_text: str,
        send_direct_message: bool = False,
    ) -> None:
        """Function which handles the /remindme command.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
            target_date (str): The date in YYYY-mm-DD HH:MM format, assuming UTC.
            reminder_text (str): The message to send with the reminder.
            send_direct_message (bool, optional): Whether or not to send a direct message to the user. Defaults to False.
        """

        await interaction.response.defer(ephemeral=True, thinking=True)
        validate_text(reminder_text)
        reminder_dt: datetime.datetime = get_date(target_date)

        reminder = Reminders(
            AuthorID=interaction.user.id,
            RemindDate=reminder_dt.strftime("%Y-%m-%d %H:%M"),
            CreationDate=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            ChannelID=interaction.channel_id,
            Message=reminder_text,
            SendDirectMessage=send_direct_message,
        )

        async with self.bot.session() as session:
            session.add(reminder)
            await session.commit()

        await interaction.followup.send(f"Reminder set for {reminder_dt}")

    async def check_reminders(self) -> None:
        """Check the database for reminders that need to be sent."""

        now = datetime.datetime.utcnow().replace(second=0, microsecond=0)

        async with self.bot.session() as session:
            query_results = (
                await session.execute(select(Reminders).where(Reminders.RemindDate <= str(now)))
            ).fetchall()

        logger.info(f"Got {len(query_results)} reminders")
        for result in query_results:
            reminder_obj = result[0]  # Access the first (and only) element in result
            author_id = reminder_obj.AuthorID
            channel_id = reminder_obj.ChannelID
            message = reminder_obj.Message
            creation_date = reminder_obj.CreationDate
            send_direct_message = reminder_obj.SendDirectMessage

            await self.respond_with_reminder(
                author_id=author_id,
                channel_id=channel_id,
                reminder_text=message,
                creation_date=creation_date,
                send_direct_message=send_direct_message,
            )

        async with self.bot.session() as session:
            await session.execute(
                delete(Reminders).where(
                    Reminders.ReminderID.in_([x[0].ReminderID for x in query_results])
                )
            )
            await session.commit()

    async def respond_with_reminder(
        self,
        author_id: int,
        channel_id: int,
        reminder_text: str,
        creation_date: str,
        send_direct_message: bool,
    ) -> None:
        """Sends a reminder to an user or channel.

        Args:
            author_id (int): The user ID to send the reminder to, if direct message is true.
            channelID (int): The channel ID to send the reminder to.
            reminder_text (str): The message provided by the user to send with the reminder.
            creation_date (str): The date of the reminder creation.
            send_direct_message (bool): Whether or not to send a direct message to the user.
        """

        target_user = self.bot.get_user(author_id)
        target_channel = self.bot.get_channel(channel_id)

        logger.info(
            f"Respond with remainder arguments: userid={author_id}, channelid={channel_id}, msg={reminder_text}"
        )

        if target_user and send_direct_message:
            await target_user.send(
                join_texts(
                    f"Direct reminder created by <@{author_id}> on {creation_date} UTC with message:",
                    f"```{reminder_text}```",
                )
            )

        if target_channel:
            await target_channel.send(  # type: ignore
                join_texts(
                    f"Direct reminder created by <@{author_id}> on {creation_date} UTC with message:",
                    f"```{reminder_text}```",
                )
            )

    @commands.Cog.listener("on_ready")
    async def set_scheduler(self) -> None:
        """Add the check_reminders function to the scheduler."""

        logger.info("check_reminders added")
        self.bot.scheduler.add_job(self.check_reminders, CronTrigger(second=0))

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        """Handle errors for application commands.

        Args:
            interaction (discord.Interaction): The interaction that triggered the error.
            error (Exception): The error that was triggered.
        """

        logger.error(type(error), error)

        match error:
            case discord.app_commands.errors.CommandOnCooldown():
                await interaction.followup.send(str(error), ephemeral=True)
            case discord.app_commands.errors.CommandInvokeError():
                await interaction.followup.send(str(error.original), ephemeral=True)


async def setup(bot: app.bot.Bot) -> None:
    """Add the Reminder cog to the bot.

    Args:
        bot (app.bot.Bot): the bot instance to which the cog should be added.
    """

    await bot.add_cog(Reminder(bot))
