from datetime import datetime, timedelta
from typing import Optional
from models.core.base.auth_base import AuthenticationBase

class Session(AuthenticationBase):
    """Session management."""
    def __init__(self, session_id: str, user_id: int, expires_in: int = 3600):
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(seconds=expires_in)
        self.is_active = True
    
    def authenticate(self) -> bool:
        """Authenticate session."""
        return self.is_active and datetime.utcnow() < self.expires_at
    
    def validate(self) -> bool:
        """Validate session data."""
        return bool(self.session_id and self.user_id)
    
    def invalidate(self) -> None:
        """Invalidate session."""
        self.is_active = False