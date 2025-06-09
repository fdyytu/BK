from abc import ABC, abstractmethod

class StatusTracker(ABC):
    """Interface untuk manajemen status."""

    @abstractmethod
    def update_status(self, status: str):
        pass