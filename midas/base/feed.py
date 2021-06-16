from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal


class DataFeed(ABC):
    @staticmethod
    @abstractmethod
    async def create(config: Any) -> DataFeed:
        pass

    @abstractmethod
    async def get_options(self, currency: str, expired: bool = False) -> list[Option]:
        pass

    @abstractmethod
    async def subscribe(self, channels: list[str]):
        pass


@dataclass(frozen=True)
class Option:
    name: str
    creation: datetime
    expiration: datetime
    strike: float
    type: Literal['call', 'put']
