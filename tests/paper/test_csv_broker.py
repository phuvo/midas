import pytest
from datetime import datetime

from midas.base import Position
from midas.paper import CsvBroker, CsvFeed, SimulatedTimer
from midas.types.order import Order


def from_iso(iso: str):
    return datetime.fromisoformat(iso.replace('Z', '+00:00'))


def create_broker(timer: SimulatedTimer):
    feed = CsvFeed(timer)
    feed.load_options(['tests/data/options.csv'])
    feed.load_tickers(['tests/data/tickers.csv'])
    return CsvBroker(timer, feed)


SYMBOL = 'ETH-2APR21-1800-C'


@pytest.mark.asyncio
async def test_sell_position():
    current_time = from_iso('2021-03-28').timestamp()
    timer = SimulatedTimer(lambda: current_time)

    broker = create_broker(timer)
    await broker.sell(Order(SYMBOL, 1, 'limit', 0.0095))

    current_time = from_iso('2021-03-28T23:35:00Z').timestamp()
    await timer.run_tasks()

    positions = await broker.get_positions('ETH')
    assert positions[0] == Position(SYMBOL, -1, 0.0095, 0.0099)


@pytest.mark.asyncio
async def test_sell_transaction():
    current_time = from_iso('2021-03-28').timestamp()
    timer = SimulatedTimer(lambda: current_time)

    broker = create_broker(timer)
    await broker.sell(Order(SYMBOL, 1, 'limit', 0.0095))

    current_time = from_iso('2021-03-28T23:35:00Z').timestamp()
    await timer.run_tasks()

    items = await broker.get_transactions('ETH', from_iso('2021-03-28'), from_iso('2021-03-29'))
    assert items[0].net_change == 0.0092
