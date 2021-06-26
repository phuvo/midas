import asyncio
from datetime import datetime
from typing import Awaitable, Callable
from midas.base.timer import Timer


class LiveTimer(Timer):
    def now(self):
        return datetime.now()

    def schedule_task(self, delay: float, task: Callable[[], Awaitable[None]]):
        callback = lambda: asyncio.create_task(task())
        asyncio.get_running_loop().call_later(delay, callback)
