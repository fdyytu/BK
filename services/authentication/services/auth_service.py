from typing import Optional, Dict, Any
from uuid import UUID
from ..interfaces.auth_strategy import AuthStrategy
from ..strategies.jwt_strategy import JWTStrategy
from ...exceptions import AuthenticationError

class AuthenticationService:
    """Authentication service."""
    
    def __init__(self, strategy: AuthStrategy):
        self.strategy = strategy
        
    async def authenticate(self, credentials: Dict[str, Any]) -> str:
        """Authenticate user and return token."""
        try:
            # Authenticate user
            user = await self.strategy.authenticate(credentials)
            
            # Generate token
            token_data = await self.strategy.create_token(user.id)
            
            return token_data.access_token
            
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")
            
    async def validate_token(self, token: str) -> Optional[UUID]:
        """Validate authentication token."""
        try:
            user = await self.strategy.validate_token(token)
            return user.id if user else None
            
        except Exception as e:
            raise AuthenticationError(f"Token validation failed: {str(e)}")