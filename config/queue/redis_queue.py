import redis
from typing import Any, Callable, Optional
from .base import BaseQueue

class RedisQueue(BaseQueue):
    """
    Redis queue provider implementation (simple list queue).
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.client = None

    def connect(self) -> None:
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)

    def publish(self, queue: str, message: Any, **kwargs) -> None:
        self.client.rpush(queue, str(message))

    def consume(self, queue: str, callback: Callable, block: bool = True, timeout: int = 0, **kwargs) -> None:
        while True:
            item = self.client.blpop(queue, timeout=timeout) if block else self.client.lpop(queue)
            if item:
                callback(item[1].decode('utf-8'))

    def close(self) -> None:
        if self.client:
            self.client.close()