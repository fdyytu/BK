from abc import ABC, abstractmethod

class PaymentCalculator(ABC):
    """Interface untuk kalkulasi pembayaran."""

    @abstractmethod
    def calculate(self, base_amount: float) -> float:
        pass