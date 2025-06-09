from typing import Optional
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..interfaces import AuthStrategy
from ..exceptions import AuthenticationError

security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware."""
    
    def __init__(self, auth_strategy: AuthStrategy):
        self.auth_strategy = auth_strategy
        
    async def __call__(self, request: Request) -> Optional[str]:
        """Process request authentication."""
        try:
            # Get token from header
            credentials: HTTPAuthorizationCredentials = await security(request)
            if not credentials:
                raise AuthenticationError("Missing authentication token")
                
            # Validate token
            user = await self.auth_strategy.validate_token(
                credentials.credentials
            )
            if not user:
                raise AuthenticationError("Invalid authentication token")
                
            # Add user to request state
            request.state.user = user
            
            return credentials.credentials
            
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")