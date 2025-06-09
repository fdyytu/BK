from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID
from .schemas import TokenData, AuthenticatedUser

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

class AuthProvider(ABC):
    """Interface for auth providers (OAuth, SSO etc)."""
    
    @abstractmethod
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user info from provider."""
        pass
        
    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> TokenData:
        """Refresh access token."""
        pass

class SessionManager(ABC):
    """Interface for session management."""
    
    @abstractmethod
    async def create_session(self, user_id: UUID) -> str:
        """Create new session."""
        pass
        
    @abstractmethod
    async def validate_session(self, session_id: str) -> Optional[UUID]:
        """Validate session."""
        pass
        
    @abstractmethod
    async def revoke_session(self, session_id: str) -> None:
        """Revoke session."""
        pass