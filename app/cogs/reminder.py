import discord
from sqlalchemy import delete
import app.bot
import datetime
import logging

from sqlalchemy.future import select
from discord.ext import commands
from discord import app_commands

from apscheduler.triggers.cron import CronTrigger
from typing import Literal
from app.database.models.reminder import Reminders

from app.utils.guilds import get_guilds

logger = logging.getLogger(__name__)


class Reminder(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    def get_remind_date(self, value: int, unit: str) -> datetime.datetime:
        if unit == "minute":
            return datetime.datetime.now() + datetime.timedelta(minutes=value)

        if unit == "hour":
            return datetime.datetime.now() + datetime.timedelta(hours=value)

        if unit == "day":
            return datetime.datetime.now() + datetime.timedelta(days=value)

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
        value: int,
        unit: Literal["minutes", "hours", "days"],
        message: str,
    ) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)

        remind_date = self.get_remind_date(value, unit).replace(second=0, microsecond=0)
        reminder = Reminders(
            UserID=str(interaction.user.id),
            RemindDate=str(remind_date),
            ChannelID=str(interaction.channel_id),
            Message=message,
        )

        async with self.bot.session() as session:
            session.add(reminder)
            await session.commit()

        await interaction.followup.send(f"Reminder set for {value} {unit}")

    async def check_reminders(self) -> None:
        now = datetime.datetime.now().replace(second=0, microsecond=0)

        async with self.bot.session() as session:
            query_results = (
                await session.execute(select(Reminders).where(Reminders.RemindDate <= str(now)))
            ).fetchall()

        logger.debug(repr(query_results))
        for result in query_results:
            reminder_obj = result[0]  # Access the first (and only) element in result
            userID = reminder_obj.UserID
            channelID = reminder_obj.ChannelID
            message = reminder_obj.Message

            logger.debug(
                f"Respond with remainder arguments: userid={userID}, channelid={channelID}, msg={message}"
            )
            await self.respond_with_reminder(
                userID=int(userID), channelID=int(channelID), message=message
            )

        async with self.bot.session() as session:
            await session.execute(
                delete(Reminders).where(
                    Reminders.ReminderID.in_([x[0].ReminderID for x in query_results])
                )
            )
            await session.commit()

    async def respond_with_reminder(self, userID: int, channelID: int, message: str) -> None:
        target_user = self.bot.get_user(userID)
        target_channel = self.bot.get_channel(channelID)

        logger.debug(
            f"responding to reminder: target_user={target_user} target_channel={target_channel}"
        )
        if target_user:
            await target_user.send(f"You have been reminded with message {message}")

        if target_channel:
            await target_channel.send(f"<@{userID}> reminder! {message}")  # type: ignore

    @commands.Cog.listener("on_ready")
    async def set_scheduler(self) -> None:
        logger.info("check_reminders added")
        self.bot.scheduler.add_job(self.check_reminders, CronTrigger(second=0))

    async def cog_app_command_error(self, interaction: discord.Interaction, error) -> None:
        logger.error(type(error), error)

        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(str(error))


async def setup(bot: app.bot.Bot) -> None:
    await bot.add_cog(Reminder(bot))
