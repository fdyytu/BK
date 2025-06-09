from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime

class IPayment(ABC):
    """Interface for payment implementations."""
    
    @abstractmethod
    async def create_payment(self,
                           amount: Decimal,
                           currency: str,
                           description: str,
                           metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create payment transaction."""
        pass
    
    @abstractmethod
    async def process_payment(self,
                            payment_id: str,
                            payment_method: str) -> Dict[str, Any]:
        """Process payment transaction."""
        pass
    
    @abstractmethod
    async def check_status(self, payment_id: str) -> Dict[str, Any]:
        """Check payment status."""
        pass
    
    @abstractmethod
    async def refund(self,
                    payment_id: str,
                    amount: Optional[Decimal] = None) -> Dict[str, Any]:
        """Process refund."""
        pass