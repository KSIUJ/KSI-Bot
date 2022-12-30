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


class Bot(commands.Bot):
    database_handler: DatabaseHandler

    def __init__(self) -> None:
        app_id = app.config.get_app_id()
        command_prefix = app.config.get_command_prefix()
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=commands.when_mentioned_or(command_prefix),  # type: ignore
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

    async def setup_hook(self) -> None:
        await create_database()
        self.database_handler = DatabaseHandler(
            app.config.get_database_path(), app.config.get_schema_path()
        )
        await setup_logging()

        await self.load_cogs()
        await self.tree.sync(guild=discord.Object(id=848921520776413213))
        await self.tree.sync(guild=discord.Object(id=528544644678680576))
        self.scheduler.start()

    async def on_message(self, message: discord.Message) -> None:
        await handle_responses(message=message)
        await super().on_message(message)

    async def close(self):
        await self.database_handler.commit()
        await super().close()
