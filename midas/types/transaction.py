from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class TradeLog:
    timestamp: datetime
    type: Literal['trade', 'delivery']
    instrument: str
    amount: float
    price: float
    net_change: float
    balance: float


Transaction = TradeLog
