from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from ..value_objects.phone_number import PhoneNumber
from ..value_objects.pulsa_amount import PulsaAmount

@dataclass
class PulsaTransaction:
    """Entity representing a pulsa transaction."""
    
    id: UUID
    phone_number: PhoneNumber
    amount: PulsaAmount
    status: str  # PENDING, SUCCESS, FAILED
    provider: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    reference_id: Optional[str] = None
    error_message: Optional[str] = None
    
    @classmethod
    def create(cls, phone_number: PhoneNumber, amount: PulsaAmount) -> 'PulsaTransaction':
        """Create new pulsa transaction."""
        return cls(
            id=uuid4(),
            phone_number=phone_number,
            amount=amount,
            status='PENDING',
            provider=phone_number.provider or 'UNKNOWN',
            created_at=datetime.utcnow()
        )
    
    def complete(self, reference_id: str) -> None:
        """Mark transaction as completed."""
        self.status = 'SUCCESS'
        self.reference_id = reference_id
        self.completed_at = datetime.utcnow()
    
    def fail(self, error_message: str) -> None:
        """Mark transaction as failed."""
        self.status = 'FAILED'
        self.error_message = error_message
        self.completed_at = datetime.utcnow()