import discord
import app.bot
import datetime
import logging

from discord.ext import commands
from discord import app_commands

from typing import Literal

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
    @app_commands.guilds(discord.Object(id=848921520776413213))
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

    async def respond_with_reminder(self, userID: int, channelID: int) -> None:
        target_user = self.bot.get_user(userID)
        target_channel = self.bot.get_channel(channelID)

        if target_user:
            await target_user.send("You have been reminded!")

        if target_channel:
            await target_channel.send(f"@{userID} you have been reminded!")  # type: ignore

    async def cog_app_command_error(self, interaction: discord.Interaction, error) -> None:
        logger.error(type(error), error)

        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(str(error))


async def setup(bot: app.bot.Bot) -> None:
    await bot.add_cog(Reminder(bot))
