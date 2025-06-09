from datetime import datetime
from typing import Optional
from .entity import AggregateRoot

class User(AggregateRoot):
    """Base user aggregate root."""
    
    def __init__(self, username: str, email: str, id: UUID = None):
        super().__init__(id)
        self._username = username
        self._email = email
        self._is_active = True
        self._last_login: Optional[datetime] = None
        
    @property
    def username(self) -> str:
        return self._username
        
    @property
    def is_active(self) -> bool:
        return self._is_active