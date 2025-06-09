from typing import Dict, Any, Optional, List
from datetime import datetime
from .voucher_interface import IVoucher
from ..common.exceptions import VoucherException

class BaseVoucher(IVoucher):
    """Base class for voucher implementations."""
    
    def __init__(self,
                 code: str,
                 discount_amount: float,
                 discount_type: str,  # FIXED or PERCENTAGE
                 start_date: datetime,
                 end_date: datetime,
                 max_uses: Optional[int] = None,
                 min_purchase: Optional[float] = None,
                 max_discount: Optional[float] = None):
        self.code = code
        self.discount_amount = discount_amount
        self.discount_type = discount_type
        self.start_date = start_date
        self.end_date = end_date
        self.max_uses = max_uses
        self.min_purchase = min_purchase
        self.max_discount = max_discount
        self.used_count = 0
        self.usage_history: List[Dict[str, Any]] = []
        
    def is_valid(self) -> bool:
        """Check if voucher is valid."""
        now = datetime.utcnow()
        
        if now < self.start_date or now > self.end_date:
            return False
            
        if self.max_uses and self.used_count >= self.max_uses:
            return False
            
        return True
    
    def can_be_used_by(self, user_id: str) -> bool:
        """Check if voucher can be used by user."""
        # Check if user has already used this voucher
        user_usage = sum(
            1 for usage in self.usage_history 
            if usage['user_id'] == user_id
        )
        return user_usage == 0
    
    def apply_discount(self, amount: float) -> float:
        """Apply voucher discount to amount."""
        if not self.is_valid():
            raise VoucherException("Voucher is not valid")
            
        if self.min_purchase and amount < self.min_purchase:
            raise VoucherException(
                f"Minimum purchase amount is {self.min_purchase}"
            )
        
        if self.discount_type == "FIXED":
            discount = self.discount_amount
        else:  # PERCENTAGE
            discount = amount * (self.discount_amount / 100)
            
        if self.max_discount:
            discount = min(discount, self.max_discount)
            
        return max(0, amount - discount)
    
    def mark_as_used(self, user_id: str, transaction_id: str) -> None:
        """Mark voucher as used."""
        if not self.is_valid():
            raise VoucherException("Voucher is not valid")
            
        if not self.can_be_used_by(user_id):
            raise VoucherException("Voucher already used by this user")
            
        self.usage_history.append({
            'user_id': user_id,
            'transaction_id': transaction_id,
            'used_at': datetime.utcnow()
        })
        
        self.used_count += 1