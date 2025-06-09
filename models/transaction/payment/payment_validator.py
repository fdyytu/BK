from abc import ABC, abstractmethod

class PaymentValidator(ABC):
    """Interface untuk validasi pembayaran."""

    @abstractmethod
    def validate(self, payment_data: dict) -> bool:
        pass