from typing import Dict, Any, Optional
from datetime import datetime
from .bill_interface import IBill
from ..transaction import Transaction

class BillBase(IBill):
    """Base class for bill implementations."""
    
    def __init__(self, 
                 provider_name: str,
                 api_key: str,
                 sandbox: bool = False):
        self.provider_name = provider_name
        self.api_key = api_key
        self.sandbox = sandbox
        self.base_url = self._get_base_url()
    
    def _get_base_url(self) -> str:
        """Get API base URL based on environment."""
        return f"https://{'sandbox' if self.sandbox else 'api'}.{self.provider_name}.com/v1"
    
    async def inquiry(self, customer_id: str) -> Dict[str, Any]:
        """Base inquiry implementation."""
        if not self.validate_customer_id(customer_id):
            raise ValueError("Invalid customer ID format")
        
        try:
            result = await self._do_inquiry(customer_id)
            return self._format_inquiry_response(result)
        except Exception as e:
            return self._format_error_response(str(e))
    
    async def pay(self, bill_id: str, amount: float) -> Dict[str, Any]:
        """Base payment implementation."""
        try:
            result = await self._do_payment(bill_id, amount)
            return self._format_payment_response(result)
        except Exception as e:
            return self._format_error_response(str(e))
    
    async def _do_inquiry(self, customer_id: str) -> Dict[str, Any]:
        """Implement actual inquiry logic in subclasses."""
        raise NotImplementedError
    
    async def _do_payment(self, bill_id: str, amount: float) -> Dict[str, Any]:
        """Implement actual payment logic in subclasses."""
        raise NotImplementedError
    
    def _format_inquiry_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format inquiry response."""
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _format_payment_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format payment response."""
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _format_error_response(self, error: str) -> Dict[str, Any]:
        """Format error response."""
        return {
            'success': False,
            'error': error,
            'timestamp': datetime.utcnow().isoformat()
        }