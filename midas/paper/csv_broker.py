from __future__ import annotations
from collections import defaultdict
from csv import DictReader
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

from midas.base import Broker, DataFeed, Option, Position, Timer
from midas.types.order import CloseOrder, Order, OrderTicket
from midas.types.transaction import TradeLog, Transaction


class CsvBroker(Broker):
    _interval = 60

    _cash: dict[str, float]
    _positions: dict[str, PositionData]
    _transactions: list[Transaction]


    def __init__(self, timer: Timer, feed: DataFeed):
        self._timer = timer
        self._feed = feed

        self._cash = defaultdict(float)
        self._positions = {}
        self._transactions = []

        self._timer.schedule_task(self._interval, self._run_worker)


    def add_cash(self, currency: str, amount: float):
        self._cash[currency] += amount


    def load_delivery_prices(self, csv_files: list[str | Path]):
        prices_lists = [read_delivery_prices(str(file_path)) for file_path in csv_files]
        self._delivery_prices = sum(prices_lists, [])


    async def get_positions(self, currency: str):
        positions: list[Position] = []
        for instrument, data in self._positions.items():
            if instrument.startswith(currency):
                item = await self._make_position(instrument, data)
                positions.append(item)
        return positions


    async def _make_position(self, instrument: str, data: PositionData):
        ticker = await self._feed.get_ticker(instrument)
        return Position(
            instrument,
            size=data.size,
            avg_price=data.avg_price,
            mark_price=ticker.mark_price,
        )


    async def close_position(self, order: CloseOrder):
        return self._create_order(('close', order))


    async def buy(self, order: Order):
        return self._create_order(('buy', order))


    async def sell(self, order: Order):
        return self._create_order(('sell', order))


    async def get_transactions(self, currency: str, start: datetime, end: datetime):
        def is_valid(item: Transaction):
            return get_currency(item.instrument) == currency and start <= item.timestamp < end
        return [item for item in self._transactions if is_valid(item)]


    def _create_order(self, form: tuple[OrderMethod, Order | CloseOrder]):
        self._execute_order(form[0], form[1])
        return OrderTicket('1', form[1].instrument, 'filled')


    def _execute_order(self, method: OrderMethod, order: Order | CloseOrder):
        assert(order.price)
        size = self._get_size(method, order)

        self._update_position(order.instrument, order.price, size)
        self._make_payment(order.instrument, order.price, size)


    def _get_size(self, method: OrderMethod, order: Order | CloseOrder):
        if type(order) is Order:
            return order.amount if method == 'buy' else -order.amount
        else:
            data = self._positions[order.instrument]
            return -data.size


    def _update_position(self, instrument: str, price: float, size: float):
        if instrument in self._positions:
            data = self._positions[instrument]
            if data.size + size == 0:
                del self._positions[instrument]
            else:
                data.size += size
        else:
            self._positions[instrument] = PositionData(size, price)


    def _make_payment(self, instrument: str, price: float, size: float):
        total = -size * price
        net_change = total - get_fee(total)

        currency = get_currency(instrument)
        self._cash[currency] += net_change

        log = TradeLog(
            timestamp =self._timer.now(),
            type      ='trade',
            instrument=instrument,
            amount    =abs(size),
            price     =price,
            net_change=net_change,
        )
        self._transactions.append(log)


    async def _run_worker(self):
        await self._check_positions()
        self._timer.schedule_task(self._interval, self._run_worker)


    async def _check_positions(self):
        expired_lists = [await self._feed.get_options(currency, expired=True) for currency in self._cash]
        expired_map = {option.name: option for option in sum(expired_lists, [])}
        open_positions: dict[str, PositionData] = {}

        for instrument in self._positions:
            data = self._positions[instrument]
            option = expired_map.get(instrument)

            if option: self._exercise(option, data.size)
            else: open_positions[instrument] = data
        self._positions = open_positions


    def _exercise(self, option: Option, size: float):
        currency = get_currency(option.name)
        delivery_price = self._get_delivery_price(currency, option.expiration)

        can_exercise_call = option.type == 'call' and option.strike < delivery_price
        can_exercise_put = option.type == 'put' and option.strike > delivery_price

        if can_exercise_call or can_exercise_put:
            price = abs(option.strike - delivery_price) / delivery_price
            change = price * size
        else:
            price = 0
            change = 0

        log = TradeLog(
            timestamp =self._timer.now(),
            type      ='delivery',
            instrument=option.name,
            amount    =abs(size),
            price     =price,
            net_change=change,
        )
        self._transactions.append(log)


    def _get_delivery_price(self, currency: str, expiry: datetime):
        date_str = expiry.date().isoformat()
        for item in self._delivery_prices:
            if item.index_name.startswith(currency) and item.date == date_str:
                return item.delivery_price
        raise ValueError


OrderMethod = Literal['buy', 'sell', 'close']


@dataclass(frozen=True)
class DeliveryPrice:
    index_name: str
    date: str
    delivery_price: float


@dataclass
class PositionData:
    size: float
    avg_price: float


def read_delivery_prices(file_path: str):
    with open(file_path) as csv_file:
        reader = DictReader(csv_file)
        return [create_delivery_price(row) for row in reader]


def create_delivery_price(row: dict[str, str]):
    return DeliveryPrice(row['Index name'], row['Date'], float(row['Delivery price']))


def get_currency(instrument: str):
    return instrument[:3]


def get_fee(total: float):
    return min(.0003, abs(total) * .125)
