from abc import ABC, abstractmethod

class Payable(ABC):
    """Interface untuk objek yang bisa dibayar."""

    @abstractmethod
    def get_amount(self) -> float:
        pass