import asyncio
from datetime import datetime
from pathlib import Path

from midas.base.timer import Timer
from midas.paper import Chronos, CsvFeed
from .strategy.short_put import ShortPut


def from_iso(iso: str):
    return datetime.fromisoformat(iso.replace('Z', '+00:00'))


def create_strategy(timer: Timer):
    data_path = Path(__file__).with_name('data')
    feed = CsvFeed(timer)
    feed.load_options([data_path / 'options.csv' ]) # type: ignore
    feed.load_tickers([data_path / '2021-W25.zip']) # type: ignore
    return ShortPut(feed, timer)


async def backtest():
    start = from_iso('2021-06-21T02:10:00Z').timestamp()
    end   = from_iso('2021-06-27T08:10:00Z').timestamp()

    chronos = Chronos()
    await chronos.add_strategy(create_strategy)
    await chronos.run(start, end)


def main():
    try:
        asyncio.get_event_loop().run_until_complete(backtest())
    except KeyboardInterrupt:
        print('Interrupted..')
