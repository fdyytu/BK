from typing import Dict, Any, Optional
import httpx
from ..entities.pulsa_transaction import PulsaTransaction
from ..value_objects.phone_number import PhoneNumber
from ..value_objects.pulsa_amount import PulsaAmount
from ...common.exceptions import ServiceError

class PulsaService:
    """Service for handling pulsa transactions."""
    
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
        return f"https://{'sandbox' if self.sandbox else 'api'}.pulsa.com/v1"
    
    async def check_balance(self) -> Dict[str, Any]:
        """Check service balance."""
        endpoint = f"{self.base_url}/balance"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                endpoint,
                headers=headers
            )
            
            if response.status_code != 200:
                raise ServiceError(f"Failed to check balance: {response.text}")
                
            return response.json()
    
    async def get_price_list(self, provider: str) -> Dict[str, Any]:
        """Get price list for provider."""
        endpoint = f"{self.base_url}/prices"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                endpoint,
                params={'provider': provider},
                headers=headers
            )
            
            if response.status_code != 200:
                raise ServiceError(f"Failed to get prices: {response.text}")
                
            return response.json()
    
    async def process_transaction(self, 
                                phone_number: str,
                                amount: float) -> PulsaTransaction:
        """Process pulsa transaction."""
        # Create value objects
        phone = PhoneNumber(phone_number)
        pulsa_amount = PulsaAmount(amount)
        
        # Create transaction
        transaction = PulsaTransaction.create(phone, pulsa_amount)
        
        try:
            # Check balance first
            balance = await self.check_balance()
            if balance['amount'] < amount:
                transaction.fail("Insufficient service balance")
                return transaction
            
            # Process transaction
            endpoint = f"{self.base_url}/topup"
            headers = self._get_headers()
            
            payload = {
                'phone': phone.formatted,
                'amount': str(pulsa_amount.amount),
                'provider': transaction.provider,
                'transaction_id': str(transaction.id)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    transaction.fail(f"Transaction failed: {response.text}")
                    return transaction
                
                result = response.json()
                
                # Monitor transaction status
                status = await self._monitor_transaction(
                    result['reference_id']
                )
                
                if status['status'] == 'SUCCESS':
                    transaction.complete(result['reference_id'])
                else:
                    transaction.fail(status.get('message', 'Transaction failed'))
                
                return transaction
                
        except Exception as e:
            transaction.fail(str(e))
            return transaction
    
    async def _monitor_transaction(self,
                                 reference_id: str,
                                 max_attempts: int = 10) -> Dict[str, Any]:
        """Monitor transaction status."""
        endpoint = f"{self.base_url}/status"
        headers = self._get_headers()
        
        for _ in range(max_attempts):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    params={'reference_id': reference_id},
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise ServiceError(
                        f"Failed to check status: {response.text}"
                    )
                    
                result = response.json()
                if result['status'] in ['SUCCESS', 'FAILED']:
                    return result
                
                await asyncio.sleep(5)
        
        return {
            'status': 'PENDING',
            'message': 'Transaction is still being processed'
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Merchant-ID': self.merchant_id,
            'Content-Type': 'application/json'
        }