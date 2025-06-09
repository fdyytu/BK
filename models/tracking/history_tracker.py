from abc import ABC, abstractmethod

class HistoryTracker(ABC):
    """Interface untuk tracking history."""

    @abstractmethod
    def get_history(self) -> list:
        pass