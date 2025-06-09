from typing import Dict, Any, Optional
from datetime import datetime
from .bill_factory import BillFactory
from ..transaction import Transaction

class BillService:
    """Service for managing bill payments."""
    
    def __init__(self, 
                 api_keys: Dict[str, str],
                 sandbox: bool = False):
        self.api_keys = api_keys
        self.sandbox = sandbox
        
    async def get_bill_details(self, 
                             bill_type: str,
                             customer_id: str) -> Dict[str, Any]:
        """Get bill details for customer."""
        try:
            handler = self._get_handler(bill_type)
            return await handler.inquiry(customer_id)
        except Exception as e:
            return self._format_error_response(str(e))
            
    async def pay_bill(self,
                      bill_type: str,
                      bill_id: str,
                      amount: float,
                      customer_id: str) -> Dict[str, Any]:
        """Process bill payment."""
        try:
            handler = self._get_handler(bill_type)
            
            # Create transaction
            transaction = Transaction(
                product_type="BILL",
                bill_type=bill_type,
                customer_id=customer_id,
                amount=amount
            )
            
            # Process payment
            result = await handler.pay(bill_id, amount)
            
            # Update transaction
            transaction.complete(result)
            
            return {
                'success': True,
                'transaction_id': transaction.id,
                'payment_details': result,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return self._format_error_response(str(e))
    
    def _get_handler(self, bill_type: str) -> BillBase:
        """Get bill payment handler."""
        api_key = self.api_keys.get(bill_type)
        
        if not api_key:
            raise ValueError(f"No API key configured for {bill_type}")
            
        return BillFactory.create(bill_type, api_key, self.sandbox)
    
    def _format_error_response(self, error: str) -> Dict[str, Any]:
        """Format error response."""
        return {
            'success': False,
            'error': error,
            'timestamp': datetime.utcnow().isoformat()
        }