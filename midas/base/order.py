from dataclasses import dataclass
from typing import Literal, Optional


OrderType = Literal['limit', 'market']
OrderState = Literal['open', 'filled', 'rejected', 'cancelled']
OrderEffect = Literal['good_til_cancelled', 'immediate_or_cancel']


@dataclass(frozen=True)
class Order:
    instrument: str
    amount: float
    type: OrderType
    price: Optional[float]
    time_in_force: OrderEffect = 'good_til_cancelled'


@dataclass(frozen=True)
class CloseOrder:
    instrument: str
    type: OrderType
    price: Optional[float]


@dataclass(frozen=True)
class OrderTicket:
    id: str
    instrument: str
    state: OrderState
