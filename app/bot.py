from __future__ import annotations

import discord
import pathlib
import app.config

from typing import List

from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.db import DatabaseHandler, create_database
from app.logger import setup_logging
from app.message_responses.responders import handle_responses
from app.utils.guilds import get_guilds


class Bot(commands.Bot):
    database_handler: DatabaseHandler

    def __init__(self) -> None:
        app_id: str = app.config.get_app_id()
        command_prefix: str = app.config.get_command_prefix()
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=commands.when_mentioned_or(command_prefix),
            intents=discord.Intents.all(),
            application_id=app_id,
        )

    async def get_list_of_cogs(self, path: str) -> List[str]:
        cogs = []
        for file in pathlib.Path(path).glob("*.py"):
            cogs.append(f"{path.replace('/', '.')}.{file.stem}")
        return cogs

    async def load_cogs(self) -> None:
        for cog in await self.get_list_of_cogs("app/cogs"):
            await self.load_extension(cog)

    async def sync_guilds(self) -> None:
        for guild in get_guilds():
            await self.tree.sync(guild=guild)

    async def setup_hook(self) -> None:
        await create_database()
        self.database_handler = DatabaseHandler(
            app.config.get_database_path(), app.config.get_schema_path()
        )
        await setup_logging()

        await self.load_cogs()
        await self.sync_guilds()
        self.scheduler.start()
        await super().setup_hook()

    async def on_message(self, message: discord.Message) -> None:
        await handle_responses(message=message)
        await super().on_message(message)

    async def close(self):
        await self.database_handler.commit()
        await super().close()
