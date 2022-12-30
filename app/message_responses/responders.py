from __future__ import annotations

import abc
import discord

from typing import Sequence


class MessageResponder(abc.ABC):
    @abc.abstractmethod
    async def get_response(self, message: discord.Message) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def set_next_responder(self, responder: MessageResponder) -> MessageResponder:
        raise NotImplementedError


class BaseMessageResponder(MessageResponder):
    _next_responder: MessageResponder

    async def set_next_responder(self, responder: MessageResponder) -> MessageResponder:
        self._next_responder = responder
        return responder


class PolishBotQuestionResponder(BaseMessageResponder):
    async def get_response(self, message: discord.Message) -> None:
        if message.content == "bocie?" or message.content.endswith(" bocie?"):
            await message.channel.send(
                f"{message.content.removesuffix('bocie?').strip()} {message.author.name}"
            )


RESPONDERS: Sequence[MessageResponder] = (PolishBotQuestionResponder(),)


async def handle_responses(message: discord.Message) -> None:
    first_responder = RESPONDERS[0]

    current_responder = first_responder
    for responder in RESPONDERS:
        current_responder = await current_responder.set_next_responder(responder)

    await first_responder.get_response(message)
