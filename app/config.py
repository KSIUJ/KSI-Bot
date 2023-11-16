import os
from typing import Iterable

import discord
import dotenv

dotenv.load_dotenv()

GUILD_IDS: frozenset[int] = frozenset((848921520776413213, 528544644678680576, 612600222622810113))
LOGGING_LEVELS: frozenset[str] = frozenset(("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"))


def get_guilds() -> Iterable[discord.Object]:
    """Returns list of discord.Object with guild ID"""

    guilds = []

    for guild_ID in GUILD_IDS:
        guilds.append(discord.Object(id=guild_ID))

    return guilds


def get_logging_level() -> str:
    """Get logging level from LOGGING_LEVEL enviromental variable

    Returns:
        str: logging level
    """

    logging_level = os.getenv("LOGGING_LEVEL")

    if logging_level not in LOGGING_LEVELS:
        raise Exception(f"Invalid logging level, valid values {LOGGING_LEVELS}")

    if logging_level is None:
        raise Exception("Enviromental variable LOGGING_LEVEL doesn't have value")

    return logging_level


def get_command_prefix() -> str:
    """Get command prefix from COMMAND_PREFIX enviromental variable"""

    command_prefix = os.getenv("COMMAND_PREFIX")

    if command_prefix is None:
        raise Exception("Enviromental variable COMMAND_PREFIX doesn't have value")

    return command_prefix


def get_app_id() -> str:
    """Get application ID from APP_ID enviromental variable"""

    app_id = os.getenv("APP_ID")

    if app_id is None:
        raise Exception("Enviromental variable APP_ID doesn't have value")

    return app_id


def get_token() -> str:
    """Get current token from DISCORD_TOKEN enviromental variable"""

    token = os.getenv("DISCORD_TOKEN")

    if token is None:
        raise Exception("Enviromental variable DISCORD_TOKEN doesn't have value")

    return token


def get_logging_path() -> str:
    """Gets logging file path from LOGS_PATH enviromental variable"""

    logging_path = os.getenv("LOGS_PATH")

    if logging_path is None:
        raise Exception("Enviromental variable for logging path doesn't have value")

    return logging_path


def get_database_path() -> str:
    """Gets database path enviromental variable"""

    db_path = os.getenv("DATABASE_PATH")

    if db_path is None:
        raise Exception("Enviromental variable for database path doesn't have value")

    return db_path


def get_data_path() -> str:
    data_path = os.getenv("DATA_PATH")

    if data_path is None:
        raise Exception("Enviromental variable for data folder path doesn't have value")

    return data_path
