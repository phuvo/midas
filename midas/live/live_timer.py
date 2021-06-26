import asyncio
import time
from datetime import datetime
from midas.base.timer import Timer, Task


class LiveTimer(Timer):
    def get_time(self):
        return time.time()

    def now(self):
        return datetime.now()

    def schedule_task(self, delay: float, task: Task):
        callback = lambda: asyncio.create_task(task())
        asyncio.get_running_loop().call_later(delay, callback)
