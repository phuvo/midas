from datetime import datetime
from typing import Callable

from midas.base import Broker, DataFeed, Strategy, Timer
from .simulated_timer import SimulatedTimer


class Chronos:
    def __init__(self, interval: float = 60):
        self._interval = interval
        self._current_time = 0
        self._timer = SimulatedTimer(lambda: self._current_time)


    def add_feed(self, create_feed: Callable[[Timer], DataFeed]):
        self._feed = create_feed(self._timer)


    def add_broker(self, create_broker: Callable[[Timer, DataFeed], Broker]):
        self._broker = create_broker(self._timer, self._feed)


    def add_strategy(self, create_strategy: Callable[[Timer, DataFeed, Broker], Strategy]):
        self._strategy = create_strategy(self._timer, self._feed, self._broker)


    async def run(self, start: float, end: float):
        self._current_time = start
        await self._strategy.on_start()
        while self._current_time < end:
            await self._timer.run_tasks()
            self._current_time += self._interval


    def get_transactions(self, currency: str, start: datetime, end: datetime):
        return self._broker.get_transactions(currency, start, end)
