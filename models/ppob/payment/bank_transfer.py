from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import httpx
from .payment_base import PaymentBase
from ..common.exceptions import PaymentError

class BankTransfer(PaymentBase):
    """Bank transfer payment implementation."""
    
    async def create_payment(self,
                           amount: Decimal,
                           currency: str,
                           description: str,
                           metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create bank transfer payment."""
        try:
            endpoint = f"{self.base_url}/bank-transfer/create"
            headers = self._get_headers()
            
            # Set expiration time (24 hours from now)
            expiration = datetime.utcnow() + timedelta(hours=24)
            
            payload = {
                'amount': str(amount),
                'currency': currency,
                'description': description,
                'metadata': metadata,
                'expiration': expiration.isoformat(),
                'type': 'bank_transfer'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise PaymentError(
                        f"Failed to create payment: {response.text}"
                    )
                    
                return response.json()
                
        except Exception as e:
            raise PaymentError(f"Payment creation failed: {str(e)}")
    
    async def process_payment(self,
                            payment_id: str,
                            payment_method: str) -> Dict[str, Any]:
        """Process bank transfer payment."""
        try:
            endpoint = f"{self.base_url}/bank-transfer/process"
            headers = self._get_headers()
            
            payload = {
                'payment_id': payment_id,
                'bank_code': payment_method,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise PaymentError(
                        f"Failed to process payment: {response.text}"
                    )
                    
                return response.json()
                
        except Exception as e:
            raise PaymentError(f"Payment processing failed: {str(e)}")
    
    async def check_status(self, payment_id: str) -> Dict[str, Any]:
        """Check bank transfer payment status."""
        endpoint = f"{self.base_url}/bank-transfer/status/{payment_id}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                endpoint,
                headers=headers
            )
            
            if response.status_code != 200:
                raise PaymentError(
                    f"Failed to check status: {response.text}"
                )
                
            return response.json()
    
    async def refund(self,
                    payment_id: str,
                    amount: Optional[Decimal] = None) -> Dict[str, Any]:
        """Process bank transfer refund."""
        try:
            endpoint = f"{self.base_url}/bank-transfer/refund"
            headers = self._get_headers()
            
            payload = {
                'payment_id': payment_id,
                'amount': str(amount) if amount else None,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise PaymentError(
                        f"Failed to process refund: {response.text}"
                    )
                    
                return response.json()
                
        except Exception as e:
            raise PaymentError(f"Refund processing failed: {str(e)}")