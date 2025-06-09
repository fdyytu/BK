from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Interface untuk pemroses pembayaran."""

    @abstractmethod
    def process_payment(self, payable):
        pass