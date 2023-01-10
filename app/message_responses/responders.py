from __future__ import annotations

import abc
import discord
import logging

from typing import Sequence

logger = logging.getLogger(__name__)


class MessageResponder(abc.ABC):
    def __init__(self) -> None:
        self._next_responder: MessageResponder | None = None

    @abc.abstractmethod
    async def get_response(self, message: discord.Message) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def set_next_responder(self, responder: MessageResponder) -> MessageResponder:
        raise NotImplementedError


class BaseMessageResponder(MessageResponder):
    async def set_next_responder(self, responder: MessageResponder) -> MessageResponder:
        self._next_responder = responder
        return responder

    async def get_response(self, message: discord.Message) -> None:
        if self._next_responder:
            await self._next_responder.get_response(message)


class PolishBotQuestionResponder(BaseMessageResponder):
    async def get_response(self, message: discord.Message) -> None:
        if message.content == "bocie?" or message.content.endswith(" bocie?"):
            await message.channel.send(
                f"{message.content.removesuffix('bocie?').strip()} {message.author.name}"
            )
        else:
            await super().get_response(message)


class WhoAskedPolishResponder(BaseMessageResponder):
    async def get_response(self, message: discord.Message) -> None:
        if "kto pytal" in message.content:
            await message.channel.send(f"<@{message.author.id}> ja pytalem!")
        else:
            await super().get_response(message)


RESPONDERS: Sequence[MessageResponder] = (PolishBotQuestionResponder(), WhoAskedPolishResponder())


async def handle_responses(message: discord.Message) -> None:
    first_responder = RESPONDERS[0]

    current_responder = first_responder
    for responder in RESPONDERS[1:]:
        current_responder = await current_responder.set_next_responder(responder)

    await first_responder.get_response(message)
