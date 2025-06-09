from datetime import datetime, timedelta
from typing import Optional
from models.core.base.auth_base import AuthenticationBase

class Token(AuthenticationBase):
    """Token management."""
    def __init__(self, token: str, expires_in: int = 3600):
        self.token = token
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(seconds=expires_in)
    
    def authenticate(self) -> bool:
        """Authenticate token."""
        return datetime.utcnow() < self.expires_at
    
    def validate(self) -> bool:
        """Validate token."""
        return bool(self.token)
    
    def refresh(self, expires_in: int = 3600) -> None:
        """Refresh token expiration."""
        self.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)