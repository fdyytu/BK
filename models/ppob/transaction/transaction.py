from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from decimal import Decimal
from pydantic import BaseModel, Field

class TransactionStatus(str, Enum):
    """Enum for transaction statuses."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    EXPIRED = "EXPIRED"

class TransactionType(str, Enum):
    """Enum for transaction types."""
    PULSA = "PULSA"
    DATA = "DATA"
    GAME = "GAME"
    BILL = "BILL"
    STREAMING = "STREAMING"
    VOUCHER = "VOUCHER"

class Transaction(BaseModel):
    """Model for PPOB transactions."""
    
    id: UUID = Field(default_factory=uuid4)
    user_id: str
    transaction_type: TransactionType
    product_code: str
    amount: Decimal
    status: TransactionStatus = TransactionStatus.PENDING
    payment_method: Optional[str] = None
    payment_details: Dict[str, Any] = Field(default_factory=dict)
    customer_number: str
    provider: str
    reference_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        """Pydantic model configuration."""
        use_enum_values = True
        json_encoders = {
            UUID: str,
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }