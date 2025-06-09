from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class IBill(ABC):
    """Interface for bill payments."""
    
    @abstractmethod
    async def inquiry(self, customer_id: str) -> Dict[str, Any]:
        """Get bill details for customer."""
        pass
    
    @abstractmethod
    async def pay(self, bill_id: str, amount: float) -> Dict[str, Any]:
        """Process bill payment."""
        pass
    
    @abstractmethod
    def validate_customer_id(self, customer_id: str) -> bool:
        """Validate customer ID format."""
        pass