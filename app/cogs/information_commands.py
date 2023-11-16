import logging

import discord
from discord import app_commands
from discord.ext import commands

import app.bot
from app.config import get_guilds

logger = logging.getLogger(__name__)


class InformationCommands(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="informator",
        description="The commands returns a link to the KSI Informator.",
    )
    @app_commands.checks.cooldown(1, 30)
    @app_commands.guilds(*get_guilds())
    async def _informator(self, interaction: discord.Interaction, public: bool = False) -> None:
        """Handles the /informator command.

        Args:
            interaction (discord.Interaction): The interaction object.
            public (bool, optional): Whether or not to send the message publicly. Defaults to False.
        """

        await interaction.response.defer(ephemeral=False, thinking=True)
        await interaction.followup.send(
            "Informator KSI: https://informator.ksi.ii.uj.edu.pl/", ephemeral=not public
        )

    @app_commands.command(
        name="baca",
        description="The commands returns a link to the website with information about Baca.",
    )
    @app_commands.checks.cooldown(1, 30)
    @app_commands.guilds(*get_guilds())
    async def _baca(self, interaction: discord.Interaction, public: bool = False) -> None:
        """Handles the /baca command.

        Args:
            interaction (discord.Interaction): The interaction object.
            public (bool, optional): Whether or not to send the message publicly. Defaults to False.
        """

        await interaction.response.defer(ephemeral=False, thinking=True)
        await interaction.followup.send(
            "Informacje na temat systemu Baca: https://sites.google.com/site/bacahelp/home",
            ephemeral=not public,
        )

    @app_commands.command(
        name="mordor",
        description="The commands returns a link to file repository Mordor.",
    )
    @app_commands.checks.cooldown(1, 30)
    @app_commands.guilds(*get_guilds())
    async def _mordor(self, interaction: discord.Interaction, public: bool = False) -> None:
        """Handles the /mordor command.

        Args:
            interaction (discord.Interaction): The interaction object.
            public (bool, optional): Whether or not to send the message publicly. Defaults to False.
        """

        await interaction.response.defer(ephemeral=False, thinking=True)
        await interaction.followup.send(
            "Repozytorium plików Mordor: https://mordor.ksi.ii.uj.edu.pl/", ephemeral=not public
        )

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        """Handles errors from the /ping command.

        Args:
            interaction (discord.Interaction): The interaction that triggered the error.
            error (Exception): The error that was triggered.
        """

        logger.error(type(error), error)

        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(str(error))

        if isinstance(
            error,
            discord.app_commands.errors.CommandInvokeError,
        ):
            logger.error(str(error))
            await interaction.followup.send(str(error.original), ephemeral=True)


async def setup(bot: app.bot.Bot) -> None:
    """Add the Reminder cog to the bot.

    Args:
        bot (app.bot.Bot): the bot instance to which the cog should be added.
    """

    await bot.add_cog(InformationCommands(bot))
