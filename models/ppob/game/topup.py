from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
from .game_service_base import GameServiceBase
from ..common.exceptions import GameServiceException

class GameTopup(GameServiceBase):
    """Game topup service implementation."""
    
    async def process_topup(self,
                           game_id: str,
                           server_id: Optional[str],
                           product_code: str,
                           quantity: int = 1) -> Dict[str, Any]:
        """Process game topup transaction."""
        # Validate game ID first
        if not await self.validate_game_id(game_id, server_id):
            raise GameServiceException("Invalid game ID or server ID")
        
        # Check balance
        balance = await self.check_balance()
        if balance['amount'] <= 0:
            raise GameServiceException("Insufficient service balance")
        
        # Process topup
        try:
            endpoint = f"{self.base_url}/topup"
            headers = self._get_headers()
            
            payload = {
                'game_id': game_id,
                'server_id': server_id,
                'product_code': product_code,
                'quantity': quantity,
                'timestamp': datetime.utcnow().isoformat(),
                'order_id': self._generate_order_id()
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise GameServiceException(
                        f"Topup failed: {response.text}"
                    )
                    
                result = response.json()
                
                # Monitor transaction status
                status = await self._monitor_transaction(
                    result['transaction_id']
                )
                
                return {
                    'success': status['status'] == 'SUCCESS',
                    'transaction_id': result['transaction_id'],
                    'order_id': payload['order_id'],
                    'status': status['status'],
                    'message': status.get('message', ''),
                    'timestamp': datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            raise GameServiceException(f"Topup failed: {str(e)}")
            
    async def _monitor_transaction(self, 
                                 transaction_id: str,
                                 max_attempts: int = 10,
                                 delay: int = 5) -> Dict[str, Any]:
        """Monitor transaction status."""
        endpoint = f"{self.base_url}/status"
        headers = self._get_headers()
        
        for attempt in range(max_attempts):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    params={'transaction_id': transaction_id},
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise GameServiceException(
                        f"Failed to check status: {response.text}"
                    )
                    
                result = response.json()
                status = result.get('status', '')
                
                if status in ['SUCCESS', 'FAILED']:
                    return result
                    
                # Wait before next attempt
                await asyncio.sleep(delay)
                
        # If we reach here, transaction is still pending
        return {
            'status': 'PENDING',
            'message': 'Transaction is still being processed'
        }
        
    def _generate_order_id(self) -> str:
        """Generate unique order ID."""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f"GAME{timestamp}{random.randint(1000, 9999)}"