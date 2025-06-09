from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID
from ...schemas import TokenData, AuthenticatedUser

class AuthStrategy(ABC):
    """Interface for authentication strategies."""
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> AuthenticatedUser:
        """Authenticate user with given credentials."""
        pass
        
    @abstractmethod
    async def create_token(self, user_id: UUID) -> TokenData:
        """Create authentication token."""
        pass
        
    @abstractmethod
    async def validate_token(self, token: str) -> Optional[AuthenticatedUser]:
        """Validate authentication token."""
        pass