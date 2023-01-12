import discord
import app.bot
import datetime
import logging

from discord.ext import commands
from discord import app_commands

from apscheduler.triggers.cron import CronTrigger
from typing import Literal

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
        await self.bot.database_handler.execute_and_commit(
            "INSERT INTO Reminders (UserID, RemindDate, ChannelID, Message) VALUES (?, ?, ?, ?)",
            interaction.user.id,
            str(remind_date),
            str(interaction.channel_id),
            message,
        )

        await interaction.followup.send(f"reminder set for {value} {unit}")

    async def check_reminders(self) -> None:
        now = datetime.datetime.now().replace(second=0, microsecond=0)

        records = await self.bot.database_handler.records(
            "SELECT ROWID, UserID, RemindDate, ChannelID, Message FROM Reminders WHERE RemindDate < ?",
            str(now),
        )
        logger.debug(repr(records))
        for _, userID, _, channelID, message in records:
            logger.debug(
                f"Respond with remainder arguments: userid={userID}, channelid={channelID}, msg={message}"
            )
            await self.respond_with_reminder(
                userID=int(userID), channelID=int(channelID), message=message
            )

        row_ids = [str(record[0]) for record in records]
        logger.debug(f"row_ids to delete {','.join(row_ids)}")

        await self.bot.database_handler.execute_and_commit(
            "DELETE FROM Reminders WHERE ROWID IN (?)", ",".join(row_ids)
        )

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
