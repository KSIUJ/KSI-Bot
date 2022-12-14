import discord
import logging
import os

from dotenv import load_dotenv
from discord.ext.commands import Bot as BotBase

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename="logs/discord.log", encoding="utf-8", mode="w"
)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class Bot(BotBase):
    def __init__(self) -> None:
        self.ready = False
        super().__init__(intents=discord.Intents.all())

    def run(self) -> None:
        load_dotenv()

        self.TOKEN = os.getenv("DISCORD_TOKEN")

        if self.TOKEN is None:
            print(
                "Token is not initialized. \
                Be sure to set environmental variable DISCORD_TOKEN",
                flush=True,
            )
            exit(1)

        try:
            super().run(self.TOKEN, reconnect=True)
            print("Bot is active.", flush=True)
        except BaseException as e:
            print(
                f"Unexpected exception while initializing bot: {type(e)}-{e}",
                flush=True,
            )
            exit(2)

    async def on_connect(self) -> None:
        print("OKBot has connected.", flush=True)

    async def on_disconnect(self) -> None:
        print("OKBot has disconnected.", flush=True)

    async def on_ready(self) -> None:
        pass

    async def on_error(self, error, *args, **kwargs) -> None:
        pass

    async def on_command_error(self, ctx, exc):
        pass

    async def on_message(self, message) -> None:
        pass


def get_bot() -> Bot:
    return Bot()
