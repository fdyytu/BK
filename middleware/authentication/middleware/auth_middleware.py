from typing import Optional
from fastapi import Request
from fastapi.security import HTTPBearer
from services.authentication.services.auth_service import AuthenticationService

security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware."""
    
    def __init__(self, auth_service: AuthenticationService):
        self.auth_service = auth_service
        
    async def __call__(self, request: Request) -> None:
        """Process request authentication."""
        # Get token from header
        credentials = await security(request)
        if not credentials:
            return None
            
        # Validate token using service
        user_id = await self.auth_service.validate_token(
            credentials.credentials
        )
        
        if user_id:
            request.state.user_id = user_id