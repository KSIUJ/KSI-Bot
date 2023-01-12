import discord
import requests
import app.bot
import logging

from io import BytesIO
from discord.ext import commands
from discord import app_commands
from app.image_builder.image_builder import ResponseImageBuilder

from app.utils.guilds import get_guilds

logger = logging.getLogger(__name__)


class ImageMaker(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="make_image",
        description="Respond with image with provided text",
    )
    @app_commands.checks.cooldown(1, 10)
    @app_commands.guilds(*get_guilds())
    async def _make_image(self, interaction: discord.Interaction, text: str, url: str) -> None:
        await interaction.response.defer(ephemeral=False, thinking=True)
        background = requests.get(url, stream=True).content
        image = ResponseImageBuilder(text=text, image=background).build()
        with BytesIO() as file:
            image.save(file, format="PNG")
            file.seek(0)
            discord_file = discord.File(file, filename="image.png")
            await interaction.followup.send(file=discord_file)

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
    await bot.add_cog(ImageMaker(bot))
