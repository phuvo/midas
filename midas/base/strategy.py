from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    async def on_start(self):
        pass
