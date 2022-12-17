from __future__ import annotations

import discord
import os


from discord.ext.commands import Bot as BotBase

from app.logger import get_logger
from app.database.db import DatabaseHandler
from dotenv import load_dotenv
from logging import Logger


class Bot(BotBase):
    instance: Bot | None = None
    database_handler: DatabaseHandler
    logger: Logger

    def __new__(cls) -> Bot:
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.ready = False

        load_dotenv()
        self._set_app_id()
        self._set_command_prefix()

        super().__init__(
            command_prefix=self.COMMAND_PREFIX,  # type: ignore
            intents=discord.Intents.all(),
            application_id=self.APP_ID,
        )

    def _set_command_prefix(self) -> None:
        """Get command prefix from COMMAND_PREFIX enviromental variable and sets command prefix variable"""

        self.COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
        if self.COMMAND_PREFIX is None:
            raise Exception("Enviromental variable COMMAND_PREFIX doesn't have value")

    def _set_app_id(self) -> None:
        """Get application ID from APP_ID enviromental variable and sets APP_ID variable"""

        self.APP_ID = os.getenv("APP_ID")
        if self.APP_ID is None:
            raise Exception("Enviromental variable APP_ID doesn't have value")

    def _set_token(self) -> None:
        """Get current token from DISCORD_TOKEN enviromental variable and sets token variable"""

        self.TOKEN = os.getenv("DISCORD_TOKEN")
        if self.TOKEN is None:
            raise Exception("Enviromental variable DISCORD_TOKEN doesn't have value")

    def _set_logger(self) -> None:
        """Gets logging file path from LOGS_PATH enviromental variable and sets logger variable"""

        self.LOGGING_PATH = os.getenv("LOGS_PATH")

        if self.LOGGING_PATH is None:
            raise Exception("Enviromental variable for logging path doesn't have value")

        self.logger = get_logger(self.LOGGING_PATH)

    def _set_database(self) -> None:
        """Gets database and schema file paths enviromental variables and sets the db variable"""

        self.DB_PATH = os.getenv("DATABASE_PATH")
        self.SCHEMA_PATH = os.getenv("SCHEMA_PATH")

        if self.DB_PATH is None:
            raise Exception("Enviromental variable for database path doesn't have value")

        if self.SCHEMA_PATH is None:
            raise Exception(
                "Enviromental variable for database schema file path doesn't have value"
            )

        self.database_handler = DatabaseHandler(self.DB_PATH, self.SCHEMA_PATH)

    def run(self) -> None:
        """Loads enviromental variables, sets token, logger and db handler and starts the bot"""

        self._set_token()
        self._set_logger()
        self._set_database()

        self.database_handler.build()
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self) -> None:
        self.logger.info("OKBot has connected")

    async def on_disconnect(self) -> None:
        self.logger.info("OKBot has disconnected")

    async def on_ready(self) -> None:
        pass

    async def on_error(self, error, *args, **kwargs) -> None:
        pass

    async def on_command_error(self, ctx, exc) -> None:
        pass

    async def on_message(self, message) -> None:
        pass


def get_bot() -> Bot:
    return Bot()
