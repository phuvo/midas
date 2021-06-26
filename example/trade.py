import asyncio
from pathlib import Path

import toml
from midas.live.deribit_feed import DeribitFeed
from midas.live.live_timer import LiveTimer

from .strategy.short_put import ShortPut


async def trade():
    config_path = Path(__file__).with_name('.env.toml')
    config = toml.load(config_path)

    feed = await DeribitFeed.create(config['broker'])
    timer = LiveTimer()

    strategy = ShortPut(feed, timer)
    await strategy.on_start()


def main():
    try:
        asyncio.get_event_loop().run_until_complete(trade())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('Interrupted..')
