from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

@dataclass(frozen=True)
class Money:
    """Value object for monetary amounts."""
    amount: Decimal
    currency: str = "IDR"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency is required")

@dataclass(frozen=True)
class Email:
    """Value object for email addresses."""
    value: str
    
    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError("Invalid email format")
            
    def _is_valid_email(self, email: str) -> bool:
        # Implement email validation
        pass

@dataclass(frozen=True)
class PhoneNumber:
    """Value object for phone numbers."""
    value: str
    country_code: str = "62"  # Indonesia
    
    def __post_init__(self):
        if not self._is_valid_phone(self.value):
            raise ValueError("Invalid phone number format")
            
    def _is_valid_phone(self, number: str) -> bool:
        # Implement phone validation
        pass