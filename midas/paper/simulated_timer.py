from __future__ import annotations
from datetime import datetime
from heapq import heappush, heappop
from typing import Callable, Tuple

from midas.base.timer import Task, Timer


class SimulatedTimer(Timer):
    _queue: list[Tuple[float, Task]]


    def __init__(self, time_func: Callable[[], float]):
        self._time_func = time_func
        self._queue = []


    def get_time(self):
        return self._time_func()


    def now(self):
        return datetime.fromtimestamp(self._time_func())


    def schedule_task(self, delay: float, task: Task):
        time = self._time_func() + delay
        heappush(self._queue, (time, task))


    async def run_tasks(self):
        while self._queue:
            time, task = self._queue[0]
            if self._time_func() < time:
                break
            heappop(self._queue)
            await task()
