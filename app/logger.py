import logging
import os
import datetime

LOGGING_PATH = "logs"


def create_logs_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def get_logger() -> logging.Logger:
    create_logs_directory(LOGGING_PATH)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename=f"{LOGGING_PATH}/{datetime.datetime.now()}.log",
        encoding="utf-8",
        mode="a+",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

    return logger
