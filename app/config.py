import os
import dotenv

dotenv.load_dotenv()


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


def get_schema_path() -> str:
    schema_path = os.getenv("SCHEMA_PATH")

    if schema_path is None:
        raise Exception("Enviromental variable for database schema file path doesn't have value")

    return schema_path


def get_data_path() -> str:
    data_path = os.getenv("DATA_PATH")

    if data_path is None:
        raise Exception("Enviromental variable for data folder path doesn't have value")

    return data_path
