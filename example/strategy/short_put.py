from __future__ import annotations
from typing import Awaitable, Callable

from midas.base import Broker, DataFeed, Option, Strategy, Timer
from midas.types.order import Order


class ShortPut(Strategy):
    CURRENCY = 'BTC'


    def __init__(self, timer: Timer, feed: DataFeed, broker: Broker):
        self.timer = timer
        self.feed = feed
        self.broker = broker


    async def on_start(self):
        await self.sell_otm_put()


    async def sell_otm_put(self):
        all_options = await self.feed.get_options(self.CURRENCY)
        option_map = {option.name: option for option in all_options}

        put_options = [option for option in all_options if option.type == 'put']
        ticker = await self.find_sellable_put(put_options)

        assert ticker
        print(f'Sold {ticker.instrument} at {ticker.bid_price}')

        sell_order = Order(ticker.instrument, 1, 'limit', ticker.bid_price)
        await self.broker.sell(sell_order)

        selected_option = option_map[ticker.instrument]
        self.run_after_expiration(self.sell_otm_put, selected_option)


    async def find_sellable_put(self, put_options: list[Option]):
        for option in put_options:
            ticker = await self.feed.get_ticker(option.name)
            if ticker.bid_price > 0: return ticker


    def run_after_expiration(self, task: Callable[[], Awaitable[None]], option: Option):
        delta = option.expiration - self.timer.now()
        self.timer.schedule_task(delta.total_seconds() + 900, task)
