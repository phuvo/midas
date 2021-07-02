from typing import Callable

from midas.base.strategy import Strategy
from midas.base.timer import Timer

from .simulated_timer import SimulatedTimer


class Chronos:
    def __init__(self, interval: float = 60):
        self._interval = interval
        self._current_time = 0
        self._timer = SimulatedTimer(lambda: self._current_time)


    async def add_strategy(self, create_strategy: Callable[[Timer], Strategy]):
        self._strategy = create_strategy(self._timer)


    async def run(self, start: float, end: float):
        self._current_time = start
        await self._strategy.on_start()
        while self._current_time < end:
            await self._timer.run_tasks()
            self._current_time += self._interval
