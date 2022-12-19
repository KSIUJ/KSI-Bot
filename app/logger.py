import pathlib
import datetime
import discord
import logging


def create_logs_directory(path: str) -> None:
    if not pathlib.Path(path).exists():
        pathlib.Path(path).mkdir()


def setup_logging(logs_path: str):
    """Creates logs directory and setups logging inside discord library"""

    create_logs_directory(logs_path)

    handler = logging.FileHandler(
        filename=f"{logs_path}/{datetime.datetime.now()}.log",
        encoding="utf-8",
        mode="w",
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    discord.utils.setup_logging(handler=handler, formatter=formatter, level=logging.DEBUG)
