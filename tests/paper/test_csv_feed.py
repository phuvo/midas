import pytest
from datetime import datetime, timezone

from midas.paper.csv_feed import CsvFeed
from midas.paper.simulated_timer import SimulatedTimer


def from_iso(iso: str):
    return datetime.fromisoformat(iso.replace('Z', '+00:00'))


@pytest.mark.asyncio
async def test_get_ticker():
    SYMBOL = 'ETH-22MAR21-1700-C'
    system_time = 0

    timer = SimulatedTimer(lambda: system_time)
    feed = CsvFeed(timer)

    feed.load_options(['tests/data/options.csv'])
    feed.load_tickers(['tests/data/tickers.csv'])

    with pytest.raises(KeyError):
        await feed.get_ticker(SYMBOL)

    system_time = from_iso('2021-03-22T00:05:00Z').timestamp()
    ticker = await feed.get_ticker(SYMBOL)
    assert ticker.timestamp.astimezone(timezone.utc) == from_iso('2021-03-22T00:03:14.018Z')
