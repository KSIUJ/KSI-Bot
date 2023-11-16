import os
from typing import Iterable

import discord
import dotenv

dotenv.load_dotenv()

GUILD_IDS: frozenset[int] = frozenset((848921520776413213, 528544644678680576, 612600222622810113))
LOGGING_LEVELS: frozenset[str] = frozenset(("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"))


class MissingEnvironmentVariable(Exception):
    pass


class InvalidEnvironmentVariable(Exception):
    pass


def get_guilds() -> Iterable[discord.Object]:
    """Get discord guilds objects based on GUILD_IDS enviromental variable

    Returns:
        Iterable[discord.Object]: iterable of discord guild objects
    """

    guilds = []

    for guild_ID in GUILD_IDS:
        guilds.append(discord.Object(id=guild_ID))

    return guilds


def get_logging_level() -> str:
    """Get logging level from LOGGING_LEVEL enviromental variable

    Raises:
        InvalidEnvironmentVariable: Invalid logging level enviromental variable
        MissingEnvironmentVariable: Missing logging level enviromental variable

    Returns:
        str: a logging level string
    """

    logging_level = os.getenv("LOGGING_LEVEL")

    if logging_level not in LOGGING_LEVELS:
        raise InvalidEnvironmentVariable(f"Invalid logging level, valid values {LOGGING_LEVELS}")

    if logging_level is None:
        raise MissingEnvironmentVariable(
            "Enviromental variable LOGGING_LEVEL doesn't have a value"
        )

    return logging_level


def get_command_prefix() -> str:
    """Get command prefix from COMMAND_PREFIX enviromental variable

    Raises:
        MissingEnvironmentVariable: missing command prefix enviromental variable

    Returns:
        str: a command prefix string
    """
    command_prefix = os.getenv("COMMAND_PREFIX")

    if command_prefix is None:
        raise MissingEnvironmentVariable(
            "Enviromental variable COMMAND_PREFIX doesn't have a value"
        )

    return command_prefix


def get_app_id() -> str:
    """Get current app id from APP_ID enviromental variable

    Raises:
        MissingEnvironmentVariable: missing app id enviromental variable

    Returns:
        str: a string with the app ID
    """

    app_id = os.getenv("APP_ID")

    if app_id is None:
        raise MissingEnvironmentVariable("Enviromental variable APP_ID doesn't have a value")

    return app_id


def get_token() -> str:
    """Get discord token from DISCORD_TOKEN enviromental variable

    Raises:
        MissingEnvironmentVariable: missing discord token enviromental variable

    Returns:
        str: a string with the discord token
    """

    token = os.getenv("DISCORD_TOKEN")

    if token is None:
        raise MissingEnvironmentVariable(
            "Enviromental variable DISCORD_TOKEN doesn't have a value"
        )

    return token


def get_logging_path() -> str:
    """Get logging path from LOGS_PATH enviromental variable

    Raises:
        MissingEnvironmentVariable: missing logging path enviromental variable

    Returns:
        str: a string with the path where the logs will be stored
    """

    logging_path = os.getenv("LOGS_PATH")

    if logging_path is None:
        raise MissingEnvironmentVariable(
            "Enviromental variable for logging path doesn't have a value"
        )

    return logging_path


def get_database_path() -> str:
    """Get database path from DATABASE_PATH enviromental variable

    Raises:
        MissingEnvironmentVariable: missing database path enviromental variable

    Returns:
        str: a string with the path where the database is present
    """

    db_path = os.getenv("DATABASE_PATH")

    if db_path is None:
        raise MissingEnvironmentVariable(
            "Enviromental variable for database path doesn't have a value"
        )

    return db_path


def get_data_path() -> str:
    """Get data path from DATA_PATH enviromental variable

    Raises:
        MissingEnvironmentVariable: missing data path enviromental variable

    Returns:
        str: a string with the path where the data folder is located in
    """

    data_path = os.getenv("DATA_PATH")

    if data_path is None:
        raise MissingEnvironmentVariable(
            "Enviromental variable for data folder path doesn't have a value"
        )

    return data_path
