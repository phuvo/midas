import pytest
from datetime import datetime

from midas.base import Position
from midas.base.order import Order
from midas.paper import CsvFeed, PaperBroker, SimulatedTimer


def from_iso(iso: str):
    return datetime.fromisoformat(iso.replace('Z', '+00:00'))


@pytest.mark.asyncio
async def test_sell_position():
    SYMBOL = 'ETH-2APR21-1800-C'
    current_time = 0

    timer = SimulatedTimer(lambda: current_time)
    feed = CsvFeed(timer)

    feed.load_options(['tests/data/options.csv'])
    feed.load_tickers(['tests/data/tickers.csv'])

    broker = PaperBroker(timer, feed)
    await broker.sell(Order(SYMBOL, 1, 'limit', 0.0095))

    current_time = from_iso('2021-03-28T23:35:00Z').timestamp()
    await timer.run_tasks()

    positions = await broker.get_positions('ETH')
    assert positions[0] == Position(SYMBOL, -1, 0.0095, 0.0099)
