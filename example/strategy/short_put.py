from typing import Awaitable, Callable

from midas.base.feed import DataFeed
from midas.base.timer import Timer


class ShortPut:
    CURRENCY = 'BTC'


    def __init__(self, feed: DataFeed, timer: Timer):
        self.feed = feed
        self.timer = timer


    async def on_start(self):
        await self.sell_otm_put()


    async def sell_otm_put(self):
        all_options = await self.feed.get_options(self.CURRENCY)
        print(len(all_options))
        self.run_after_expiration(self.sell_otm_put)


    def run_after_expiration(self, task: Callable[[], Awaitable[None]]):
        """
        Schedule a task to run after daily options' expiration time, at 08:05 UTC.
        """
        self.timer.schedule_task(15, task)
