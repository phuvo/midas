from __future__ import annotations
from collections import defaultdict

from midas.base import Broker, DataFeed, Timer
from midas.base.order import CloseOrder, Order


class PaperBroker(Broker):
    def __init__(self, timer: Timer, feed: DataFeed):
        self._timer = timer
        self._feed = feed

        self._cash = defaultdict(float)


    def add_cash(self, currency: str, amount: float):
        self._cash[currency] += amount


    async def get_positions(self, currency: str):
        pass


    async def close_position(self, order: CloseOrder):
        pass


    async def buy(self, order: Order):
        pass


    async def sell(self, order: Order):
        pass
