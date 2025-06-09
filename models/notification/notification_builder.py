from abc import ABC, abstractmethod

class NotificationBuilder(ABC):
    """Interface untuk pembuatan notifikasi."""

    @abstractmethod
    def build(self, template: str, context: dict) -> str:
        pass