from __future__ import annotations

import discord
import pathlib
import app.config

from typing import List

from discord.ext import commands

from app.database.db import DatabaseHandler
from app.logger import setup_logging


class Bot(commands.Bot):
    database_handler: DatabaseHandler

    def __init__(self) -> None:
        app_id = app.config.get_app_id()
        command_prefix = app.config.get_command_prefix()

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
        await setup_logging()

        self.database_handler = DatabaseHandler(
            app.config.get_database_path(), app.config.get_schema_path()
        )
        await self.database_handler.build()

        await self.load_cogs()
        await self.tree.sync(guild=discord.Object(id=848921520776413213))

    async def close(self):
        await self.database_handler.commit()
        await super().close()
