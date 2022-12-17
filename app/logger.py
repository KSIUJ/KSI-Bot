import logging
import pathlib
import datetime


def create_logs_directory(path: str) -> None:
    if not pathlib.Path(path).exists():
        pathlib.Path(path).mkdir()


def get_logger(logs_path: str) -> logging.Logger:
    """Creates logs directory and return a logger object connected to this directory"""

    create_logs_directory(logs_path)
    logger = logging.getLogger("discord")
    logger.setLevel("DEBUG")
    handler = logging.FileHandler(
        filename=f"{logs_path}/{datetime.datetime.now()}.log",
        encoding="utf-8",
        mode="a+",
    )
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger
