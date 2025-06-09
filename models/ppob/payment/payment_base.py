from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime
import httpx
from .payment_interface import IPayment
from ..common.exceptions import PaymentError

class PaymentBase(IPayment):
    """Base class for payment implementations."""
    
    def __init__(self, 
                 api_key: str,
                 merchant_id: str,
                 sandbox: bool = False):
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.sandbox = sandbox
        self.base_url = self._get_base_url()
    
    def _get_base_url(self) -> str:
        """Get API base URL based on environment."""
        return f"https://{'sandbox' if self.sandbox else 'api'}.payment.com/v1"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Merchant-ID': self.merchant_id,
            'Content-Type': 'application/json'
        }