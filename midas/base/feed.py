from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Literal
from .ticker import Ticker


class DataFeed(ABC):
    @abstractmethod
    async def get_options(self, currency: str, expired: bool = False) -> list[Option]:
        """Return all options, sorted by expirate date and strike price."""
        pass

    @abstractmethod
    async def subscribe(self, channels: list[str], on_message: OnMessage):
        pass

    @abstractmethod
    async def get_ticker(self, instrument: str) -> Ticker:
        pass


@dataclass(frozen=True)
class Option:
    name: str
    creation: datetime
    expiration: datetime
    strike: int
    type: Literal['call', 'put']


OnMessage = Callable[[Dict[str, Any]], None]
