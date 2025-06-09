from typing import Any, Callable
from .base import BaseQueue

class InMemoryQueue(BaseQueue):
    """
    In-memory mock queue for testing/development.
    """
    def __init__(self):
        self.queues = {}

    def connect(self) -> None:
        pass

    def publish(self, queue: str, message: Any, **kwargs) -> None:
        self.queues.setdefault(queue, []).append(message)

    def consume(self, queue: str, callback: Callable, **kwargs) -> None:
        for msg in self.queues.get(queue, []):
            callback(msg)
        self.queues[queue] = []

    def close(self) -> None:
        self.queues.clear()