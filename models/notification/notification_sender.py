from abc import ABC, abstractmethod

class NotificationSender(ABC):
    """Interface untuk pengiriman notifikasi."""

    @abstractmethod
    def send(self, recipient, message: str):
        pass