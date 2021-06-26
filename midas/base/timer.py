from abc import ABC, abstractmethod
from datetime import datetime
from typing import Awaitable, Callable


class Timer(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass

    @abstractmethod
    def schedule_task(self, delay: float, task: Callable[[], Awaitable[None]]):
        pass
