from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_voucher import BaseVoucher

class GameVoucher(BaseVoucher):
    """Game-specific voucher implementation."""
    
    def __init__(self,
                 code: str,
                 discount_amount: float,
                 discount_type: str,
                 start_date: datetime,
                 end_date: datetime,
                 game_id: str,
                 platform: str,
                 region: Optional[str] = None,
                 **kwargs):
        super().__init__(
            code=code,
            discount_amount=discount_amount,
            discount_type=discount_type,
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
        self.game_id = game_id
        self.platform = platform
        self.region = region
        
    def can_be_used_by(self, user_id: str) -> bool:
        """Check if voucher can be used by user."""
        # First check base conditions
        if not super().can_be_used_by(user_id):
            return False
            
        # Add game-specific validation here
        # For example, check if user has the game installed
        # or if user is in the correct region
        return True
        
    def apply_discount(self, amount: float) -> float:
        """Apply game voucher discount."""
        # Add game-specific discount logic here
        return super().apply_discount(amount)