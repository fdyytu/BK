from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseQueue(ABC):
    """
    Abstract base class for queue providers.
    All queue backends must implement this interface for consistency.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the queue backend."""
        pass

    @abstractmethod
    def publish(self, queue: str, message: Any, **kwargs) -> None:
        """Publish a message to a specific queue or topic."""
        pass

    @abstractmethod
    def consume(self, queue: str, callback, **kwargs) -> None:
        """
        Start consuming messages from a queue or topic.
        :param queue: Name of the queue/topic.
        :param callback: Function to call for each message.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the connection to the queue backend."""
        pass