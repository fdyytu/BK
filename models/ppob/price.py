from typing import Dict, Any
from datetime import datetime

class Price:
    """Price implementation with history tracking."""
    
    def __init__(self, amount: float, currency: str = "IDR"):
        self.amount = amount
        self.currency = currency
        self.history: List[Dict[str, Any]] = []
        self._record_change(amount)
    
    def update(self, new_amount: float) -> None:
        """Update price amount."""
        self._record_change(new_amount)
        self.amount = new_amount
    
    def _record_change(self, amount: float) -> None:
        """Record price change in history."""
        self.history.append({
            'amount': amount,
            'timestamp': datetime.utcnow()
        })
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get price change history."""
        return sorted(
            self.history,
            key=lambda x: x['timestamp'],
            reverse=True
        )