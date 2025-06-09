from abc import ABC, abstractmethod

class Notifiable(ABC):
    """Interface untuk objek yang bisa dinotifikasi."""

    @abstractmethod
    def notify(self, message: str):
        pass