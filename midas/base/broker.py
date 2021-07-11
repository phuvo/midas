from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from midas.types.order import CloseOrder, Order, OrderTicket


class Broker(ABC):
    @abstractmethod
    async def get_positions(self, currency: str) -> list[Position]:
        pass

    @abstractmethod
    async def close_position(self, order: CloseOrder) -> OrderTicket:
        pass

    @abstractmethod
    async def buy(self, order: Order) -> OrderTicket:
        pass

    @abstractmethod
    async def sell(self, order: Order) -> OrderTicket:
        pass


@dataclass(frozen=True)
class Position:
    instrument: str
    size: float
    avg_price: float
    mark_price: float
