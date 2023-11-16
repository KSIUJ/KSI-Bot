from __future__ import annotations

import pathlib

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import app.config
from app.database.database_handler import DatabaseHandler, create_database_directory
from app.logger import setup_logging
from app.message_responses.responders import handle_responses


class Bot(commands.Bot):
    """Bot wrapper around the discord Bot class."""

    def __init__(self) -> None:
        app_id: str = app.config.get_app_id()
        command_prefix: str = app.config.get_command_prefix()

        super().__init__(
            command_prefix=commands.when_mentioned_or(command_prefix),
            intents=discord.Intents.all(),
            application_id=app_id,
        )

    async def get_list_of_cogs(self, path: str) -> list[str]:
        """Get a list of cogs from a given path.

        Args:
            path (str): The path to the cogs directory.

        Returns:
            list[str]: A list of cogs.
        """

        python_files = pathlib.Path(path).glob("*.py")
        return [f"{path.replace('/', '.')}.{file.stem}" for file in python_files]

    async def load_cogs(self) -> None:
        """Load all cogs from the cogs directory."""

        for cog in await self.get_list_of_cogs("app/cogs"):
            await self.load_extension(cog)

    async def sync_guilds(self) -> None:
        """Sync the guilds the bot is in with the database."""

        for guild in app.config.get_guilds():
            await self.tree.sync(guild=guild)

    async def setup_hook(self) -> None:
        """Perform asynchronous setup after the bot is logged in."""
        await setup_logging(level=app.config.get_logging_level())

        create_database_directory(database_path=app.config.get_database_path())
        self.database_handler = DatabaseHandler(database_path=app.config.get_database_path())
        await self.database_handler.create_database()
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()

        await self.load_cogs()
        await self.sync_guilds()

        self.scheduler.start()
        await super().setup_hook()

    async def on_message(self, message: discord.Message) -> None:
        """Executes when a message is sent in a channel the bot can see."""

        await handle_responses(message=message)
        await super().on_message(message)

    async def close(self) -> None:
        """Called when the bot is shutting down."""

        await super().close()

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        """Async session for the database."""

        return self.database_handler.session
