import asyncio
from datetime import datetime
from pathlib import Path

from midas.base import DataFeed, Timer
from midas.paper import Chronos, CsvBroker, CsvFeed
from .strategy import ShortPut


data_path = Path(__file__).with_name('data')


def from_iso(iso: str):
    return datetime.fromisoformat(iso.replace('Z', '+00:00'))


def create_feed(timer: Timer):
    feed = CsvFeed(timer)
    feed.load_options([data_path / 'options.csv' ])
    feed.load_tickers([data_path / '2021-W25.zip'])
    return feed


def create_broker(timer: Timer, feed: DataFeed):
    broker = CsvBroker(timer, feed)
    broker.load_delivery_prices([data_path / 'delivery_prices.csv'])
    broker.add_cash('BTC', 0.02)
    return broker


async def backtest():
    start = from_iso('2021-06-21T02:10:00Z').timestamp()
    end   = from_iso('2021-06-27T08:10:00Z').timestamp()

    chronos = Chronos()
    chronos.add_feed(create_feed)
    chronos.add_broker(create_broker)
    chronos.add_strategy(ShortPut)
    await chronos.run(start, end)


def main():
    try:
        asyncio.get_event_loop().run_until_complete(backtest())
    except KeyboardInterrupt:
        print('Interrupted..')
