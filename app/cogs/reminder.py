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
from app.config import get_guilds
from app.database.models.reminder import Reminders

logger = logging.getLogger(__name__)


class Reminder(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    def get_remind_date(self, value: int, unit: str) -> datetime.datetime:
        """Converts arguments from /remindme to a datetime object.

        Args:
            value (int): The value of the reminder.
            unit (str): The unit of the reminder.

        Returns:
            datetime.datetime: The date of the reminder.
        """

        match unit:
            case "minute":
                return datetime.datetime.now() + datetime.timedelta(minutes=value)
            case "hour":
                return datetime.datetime.now() + datetime.timedelta(hours=value)
            case "day":
                return datetime.datetime.now() + datetime.timedelta(days=value)
            case _:
                return datetime.datetime.now()

    @app_commands.command(
        name="remindme",
        description="set a reminder",
    )
    @app_commands.checks.cooldown(1, 30)
    @app_commands.guilds(*get_guilds())
    async def _remindme(
        self,
        interaction: discord.Interaction,
        value: app_commands.Range[int, 1, 366 * 3],
        unit: Literal["minutes", "hours", "days"],
        message: str,
        send_direct_message: bool = False,
    ) -> None:
        """Function which handles the /remindme command.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
            value (app_commands.Range[int, 1, 366 * 3]): The value of the reminder.
            unit (Literal["minutes", "hours", "days"]): The unit of the reminder.
            message (str): The message to send with the reminder.
            send_direct_message (bool, optional): Whether or not to send a direct message to the user. Defaults to False.
        """

        await interaction.response.defer(ephemeral=True, thinking=True)

        remind_date = self.get_remind_date(value, unit).replace(second=0, microsecond=0)
        reminder = Reminders(
            AuthorID=str(interaction.user.id),
            RemindDate=remind_date.strftime("%Y-%m-%d %H:%M"),
            CreationDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            ChannelID=str(interaction.channel_id),
            Message=message,
            SendDirectMessage=send_direct_message,
        )

        async with self.bot.session() as session:
            session.add(reminder)
            await session.commit()

        await interaction.followup.send(f"Reminder set for {value} {unit}")

    async def check_reminders(self) -> None:
        """Check the database for reminders that need to be sent."""

        now = datetime.datetime.now().replace(second=0, microsecond=0)

        async with self.bot.session() as session:
            query_results = (
                await session.execute(select(Reminders).where(Reminders.RemindDate <= str(now)))
            ).fetchall()

        logger.info(f"Got {len(query_results)} reminders")
        for result in query_results:
            reminder_obj = result[0]  # Access the first (and only) element in result
            userID = reminder_obj.AuthorID
            channelID = reminder_obj.ChannelID
            message = reminder_obj.Message
            creation_date = reminder_obj.CreationDate
            send_direct_message = reminder_obj.SendDirectMessage

            await self.respond_with_reminder(
                userID=int(userID),
                channelID=int(channelID),
                message=message,
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
        userID: int,
        channelID: int,
        message: str,
        creation_date: str,
        send_direct_message: bool,
    ) -> None:
        """Sends a reminder to an user or channel.

        Args:
            userID (int): The user ID to send the reminder to, if direct message is true.
            channelID (int): The channel ID to send the reminder to.
            message (str): The message provided by the user to send with the reminder.
            creation_date (str): The date of the reminder creation.
            send_direct_message (bool): Whether or not to send a direct message to the user.
        """

        target_user = self.bot.get_user(userID)
        target_channel = self.bot.get_channel(channelID)

        logger.info(
            f"Respond with remainder arguments: userid={userID}, channelid={channelID}, msg={message}"
        )

        if target_user and send_direct_message:
            await target_user.send(
                f"Direct reminder created by <@{userID}> on {creation_date} with message: {message}"
            )

        if target_channel:
            await target_channel.send(  # type: ignore
                f"Reminder created by <@{userID}> on {creation_date} with message: {message}"
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

        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(str(error))


async def setup(bot: app.bot.Bot) -> None:
    """Add the Reminder cog to the bot.

    Args:
        bot (app.bot.Bot): the bot instance to which the cog should be added.
    """

    await bot.add_cog(Reminder(bot))
