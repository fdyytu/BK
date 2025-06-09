from abc import ABC, abstractmethod

class Trackable(ABC):
    """Interface untuk tracking status."""

    @abstractmethod
    def get_status(self) -> str:
        pass