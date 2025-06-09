from typing import Dict, Any, Optional
import httpx
from datetime import datetime

class DigiflazzAPI:
    """Digiflazz API integration."""
    
    def __init__(self, api_key: str, username: str, base_url: str):
        self.api_key = api_key
        self.username = username
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def check_balance(self) -> Dict[str, Any]:
        """Check deposit balance."""
        endpoint = f"{self.base_url}/cek-saldo"
        payload = self._create_payload()
        
        async with self.client:
            response = await self.client.post(endpoint, json=payload)
            return response.json()
    
    async def price_list(self, type: str = "all") -> Dict[str, Any]:
        """Get product price list."""
        endpoint = f"{self.base_url}/price-list"
        payload = self._create_payload({"type": type})
        
        async with self.client:
            response = await self.client.post(endpoint, json=payload)
            return response.json()
    
    async def topup(self, 
                   customer_no: str,
                   product_code: str,
                   ref_id: str) -> Dict[str, Any]:
        """Process topup transaction."""
        endpoint = f"{self.base_url}/transaction"
        payload = self._create_payload({
            "customer_no": customer_no,
            "product_code": product_code,
            "ref_id": ref_id
        })
        
        async with self.client:
            response = await self.client.post(endpoint, json=payload)
            return response.json()
    
    def _create_payload(self, additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create API payload with signature."""
        payload = {
            "username": self.username,
            "sign": self._generate_signature()
        }
        
        if additional_data:
            payload.update(additional_data)
            
        return payload
    
    def _generate_signature(self) -> str:
        """Generate API signature."""
        # Implement signature generation logic
        pass