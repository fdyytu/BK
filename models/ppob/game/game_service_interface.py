from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

class IGameService(ABC):
    """Interface for game service implementations."""
    
    @abstractmethod
    async def validate_game_id(self, game_id: str, server_id: Optional[str] = None) -> bool:
        """Validate game ID and server ID."""
        pass
    
    @abstractmethod
    async def get_product_list(self, game_id: str) -> List[Dict[str, Any]]:
        """Get available products for game."""
        pass
    
    @abstractmethod
    async def check_balance(self) -> Dict[str, Any]:
        """Check service balance."""
        pass
    
    @abstractmethod
    async def process_topup(self, 
                           game_id: str,
                           server_id: Optional[str],
                           product_code: str,
                           quantity: int = 1) -> Dict[str, Any]:
        """Process game topup."""
        pass