from __future__ import annotations

import abc


class MessageParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_response(self, message: str) -> str | None:
        pass

    @abc.abstractmethod
    def set_next_responder(self, responder: MessageParser) -> None:
        pass
