from abc import ABC, abstractmethod
from datetime import datetime
from typing import Awaitable, Callable


Task = Callable[[], Awaitable[None]]

class Timer(ABC):
    @abstractmethod
    def get_time(self) -> float:
        pass

    @abstractmethod
    def now(self) -> datetime:
        pass

    @abstractmethod
    def schedule_task(self, delay: float, task: Task):
        pass
