from abc import ABC, abstractmethod
from typing import Any, Callable

class AsyncBaseQueue(ABC):
    """
    Abstract base class for async queue providers.
    """
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def publish(self, queue: str, message: Any, **kwargs) -> None:
        pass

    @abstractmethod
    async def consume(self, queue: str, callback: Callable, **kwargs) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass