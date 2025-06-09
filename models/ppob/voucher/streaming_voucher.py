from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_voucher import BaseVoucher

class StreamingVoucher(BaseVoucher):
    """Streaming service voucher implementation."""
    
    def __init__(self,
                 code: str,
                 discount_amount: float,
                 discount_type: str,
                 start_date: datetime,
                 end_date: datetime,
                 service_provider: str,
                 subscription_type: str,
                 min_subscription_months: int = 1,
                 **kwargs):
        super().__init__(
            code=code,
            discount_amount=discount_amount,
            discount_type=discount_type,
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
        self.service_provider = service_provider
        self.subscription_type = subscription_type
        self.min_subscription_months = min_subscription_months
        
    def can_be_used_by(self, user_id: str) -> bool:
        """Check if voucher can be used by user."""
        # First check base conditions
        if not super().can_be_used_by(user_id):
            return False
            
        # Add streaming-specific validation here
        # For example, check if user doesn't already have an active subscription
        return True
        
    def apply_discount(self, amount: float) -> float:
        """Apply streaming voucher discount."""
        # Add streaming-specific discount logic here
        return super().apply_discount(amount)