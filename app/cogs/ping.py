import discord
import app.bot
import logging
import aiohttp

from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)


class Pinger(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="ping a website and check if it does work for the bot",
    )
    @app_commands.checks.cooldown(1, 10)
    @app_commands.guilds(
        discord.Object(id=848921520776413213), discord.Object(id=528544644678680576)
    )
    async def _ping(self, interaction: discord.Interaction, url: str) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)

        if "http" not in url:
            url = f"http://{url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status

        await interaction.followup.send(f"Provided URL returned status {status}")

    async def cog_app_command_error(self, interaction: discord.Interaction, error) -> None:
        logger.error(type(error), error)

        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(str(error))

        if isinstance(
            error,
            discord.app_commands.errors.CommandInvokeError,
        ):
            logger.error(str(error))
            await interaction.followup.send(str(error.original))


async def setup(bot: app.bot.Bot) -> None:
    await bot.add_cog(Pinger(bot))
