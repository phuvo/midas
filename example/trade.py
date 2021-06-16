from pathlib import Path
import asyncio

from midas.live.deribit_feed import DeribitFeed
import toml


async def trade():
    config_path = Path(__file__).with_name('.env.toml')
    config = toml.load(config_path)

    feed = await DeribitFeed.create(config['broker'])
    options = await feed.get_options('BTC')
    print(len(options))


def main():
    asyncio.run(trade())
