from __future__ import annotations
from collections import defaultdict
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path

from midas.base import Broker, DataFeed, Timer
from midas.base.order import CloseOrder, Order


class PaperBroker(Broker):
    def __init__(self, timer: Timer, feed: DataFeed):
        self._timer = timer
        self._feed = feed

        self._cash = defaultdict(float)


    def add_cash(self, currency: str, amount: float):
        self._cash[currency] += amount


    def load_delivery_prices(self, csv_files: list[str | Path]):
        prices_lists = [read_delivery_prices(str(file_path)) for file_path in csv_files]
        self._delivery_prices = sum(prices_lists, [])


    async def get_positions(self, currency: str):
        pass


    async def close_position(self, order: CloseOrder):
        pass


    async def buy(self, order: Order):
        pass


    async def sell(self, order: Order):
        pass


@dataclass(frozen=True)
class DeliveryPrice:
    index_name: str
    date: str
    delivery_price: float


def read_delivery_prices(file_path: str):
    with open(file_path) as csv_file:
        reader = DictReader(csv_file)
        return [create_delivery_price(row) for row in reader]


def create_delivery_price(row: dict[str, str]):
    return DeliveryPrice(row['Index name'], row['Date'], float(row['Delivery price']))
