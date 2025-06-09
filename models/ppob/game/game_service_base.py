from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
from .game_service_interface import IGameService
from ..common.exceptions import GameServiceException

class GameServiceBase(IGameService):
    """Base implementation for game services."""
    
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
        return f"https://{'sandbox' if self.sandbox else 'api'}.gameservice.com/v1"
        
    async def validate_game_id(self, 
                             game_id: str,
                             server_id: Optional[str] = None) -> bool:
        """Validate game ID and server ID."""
        try:
            endpoint = f"{self.base_url}/validate"
            headers = self._get_headers()
            
            payload = {
                'game_id': game_id,
                'server_id': server_id
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    return False
                    
                result = response.json()
                return result.get('valid', False)
                
        except Exception:
            return False
            
    async def get_product_list(self, game_id: str) -> List[Dict[str, Any]]:
        """Get available products for game."""
        endpoint = f"{self.base_url}/products"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                endpoint,
                params={'game_id': game_id},
                headers=headers
            )
            
            if response.status_code != 200:
                raise GameServiceException(
                    f"Failed to get products: {response.text}"
                )
                
            return response.json().get('products', [])
            
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
                raise GameServiceException(
                    f"Failed to check balance: {response.text}"
                )
                
            return response.json()
            
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Merchant-ID': self.merchant_id,
            'Content-Type': 'application/json'
        }