import logging

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

import app.bot
from app.config import get_guilds

logger = logging.getLogger(__name__)


class Pinger(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="ping a website and check if it does work for the bot",
    )
    @app_commands.checks.cooldown(1, 30)
    @app_commands.guilds(*get_guilds())
    async def _ping(self, interaction: discord.Interaction, url: str) -> None:
        """Handles the /ping command.
        The commands pings a website and checks if it does work for the bot.

        Args:
            interaction (discord.Interaction): The interaction object.
            url (str): The url to ping.
        """

        await interaction.response.defer(ephemeral=False, thinking=True)

        if "http" not in url:
            url = f"http://{url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status

        await interaction.followup.send(f"Provided URL returned status {status}")

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        """Handles errors from the /ping command.

        Args:
            interaction (discord.Interaction): The interaction that triggered the error.
            error (Exception): The error that was triggered.
        """

        logger.error(type(error), error)
        match error:
            case discord.app_commands.errors.CommandOnCooldown():
                await interaction.response.send_message(str(error))
            case discord.app_commands.errors.CommandInvokeError():
                await interaction.followup.send(str(error.original), ephemeral=True)
            case _:
                await interaction.followup.send(str(error), ephemeral=True)


async def setup(bot: app.bot.Bot) -> None:
    """Add the Reminder cog to the bot.

    Args:
        bot (app.bot.Bot): the bot instance to which the cog should be added.
    """

    await bot.add_cog(Pinger(bot))
