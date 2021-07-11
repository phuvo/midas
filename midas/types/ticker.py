from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict

from midas.helpers.datetime import from_ms


class TickerDict(TypedDict):
    instrument_name : str
    timestamp       : int
    best_bid_price  : float
    mark_price      : float
    best_ask_price  : float
    underlying_price: float


@dataclass(frozen=True)
class Ticker:
    instrument: str
    timestamp : datetime
    bid_price : float
    mark_price: float
    ask_price : float
    underlying_price: float


def create_ticker(ticker: TickerDict):
    return Ticker(
        instrument=ticker['instrument_name'],
        timestamp =from_ms(ticker['timestamp']),
        bid_price =ticker['best_bid_price'],
        mark_price=ticker['mark_price'],
        ask_price =ticker['best_ask_price'],
        underlying_price=ticker['underlying_price'],
    )
