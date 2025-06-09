from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class IVoucher(ABC):
    """Interface for voucher implementations."""
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Check if voucher is valid."""
        pass
    
    @abstractmethod
    def can_be_used_by(self, user_id: str) -> bool:
        """Check if voucher can be used by user."""
        pass
    
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        """Apply voucher discount to amount."""
        pass
    
    @abstractmethod
    def mark_as_used(self, user_id: str, transaction_id: str) -> None:
        """Mark voucher as used."""
        pass