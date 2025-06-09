from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID
from models.core.base.entity import AggregateRoot
from .payment_status import PaymentStatus
from .payment_method import PaymentMethod
from .money import Money
from .exceptions import InvalidPaymentStateError

class Payment(AggregateRoot):
    """Payment aggregate root."""
    
    def __init__(
        self,
        amount: Money,
        method: PaymentMethod,
        reference: str,
        id: UUID = None
    ):
        super().__init__(id)
        self._amount = amount
        self._method = method
        self._reference = reference
        self._status = PaymentStatus.PENDING
        self._processed_at: Optional[datetime] = None
        
    @property
    def amount(self) -> Money:
        return self._amount
        
    @property
    def status(self) -> PaymentStatus:
        return self._status
        
    def process(self) -> None:
        """Process the payment."""
        if self._status != PaymentStatus.PENDING:
            raise InvalidPaymentStateError(
                f"Cannot process payment in {self._status} state"
            )
        self._status = PaymentStatus.PROCESSING
        
    def complete(self) -> None:
        """Mark payment as completed."""
        if self._status != PaymentStatus.PROCESSING:
            raise InvalidPaymentStateError(
                f"Cannot complete payment in {self._status} state"
            )
        self._status = PaymentStatus.COMPLETED
        self._processed_at = datetime.utcnow()