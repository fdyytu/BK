from typing import Dict, Any, Optional
import re
from datetime import datetime
from .bill_base import BillBase

class PDAMBill(BillBase):
    """PDAM bill payment implementation."""
    
    def __init__(self, api_key: str, sandbox: bool = False):
        super().__init__("pdam", api_key, sandbox)
        
    def validate_customer_id(self, customer_id: str) -> bool:
        """Validate PDAM customer ID format."""
        # PDAM number format: 10-12 digits
        return bool(re.match(r'^\d{10,12}$', customer_id))
    
    async def _do_inquiry(self, customer_id: str) -> Dict[str, Any]:
        """Process PDAM inquiry."""
        endpoint = f"{self.base_url}/bills/pdam/inquiry"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint,
                json={
                    'customer_id': customer_id,
                    'area_code': self._get_area_code(customer_id)
                },
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"PDAM Inquiry failed: {response.text}")
                
            return response.json()
    
    async def _do_payment(self, bill_id: str, amount: float) -> Dict[str, Any]:
        """Process PDAM payment."""
        endpoint = f"{self.base_url}/bills/pdam/payment"
        headers = self._get_headers()
        
        payload = {
            'bill_id': bill_id,
            'amount': amount,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint,
                json=payload,
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"PDAM Payment failed: {response.text}")
                
            return response.json()
    
    def _get_area_code(self, customer_id: str) -> str:
        """Extract area code from customer ID."""
        return customer_id[:4]
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }