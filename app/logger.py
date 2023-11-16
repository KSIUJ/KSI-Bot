import datetime
import logging
import pathlib

import discord

from app.config import get_data_path, get_logging_path


async def create_logs_directory(path: str) -> None:
    """Creates logs directory if it doesn't exist

    Args:
        path (str): path to the logs directory
    """

    if not pathlib.Path(get_data_path()).exists():
        pathlib.Path(get_data_path()).mkdir()

    if not pathlib.Path(path).exists():
        pathlib.Path(path).mkdir()


async def setup_logging(level: str) -> None:
    """Creates logs directory and setups logging inside discord library

    Args:
        level (str): logging level
    """

    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    logging_level = level_mapping[level]

    await create_logs_directory(get_logging_path())
    handler = get_handler()
    formatter = get_formatter()
    discord.utils.setup_logging(handler=handler, formatter=formatter, level=logging_level)


def get_formatter() -> logging.Formatter:
    """Returns logging formatter which formats the output of logging information

    Returns:
        logging.Formatter: a logging formatter object.
    """

    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", date_format, style="{"
    )
    return formatter


def get_handler() -> logging.Handler:
    """Returns logging handler which manages the output of logging information

    Returns:
        logging.Handler: a logging handler object.
    """

    logs_path = get_logging_path()
    handler = logging.FileHandler(
        filename=f"{logs_path}/{datetime.datetime.now()}.log",
        encoding="utf-8",
        mode="w",
    )
    return handler
