from abc import ABC
from typing import Any
from datetime import datetime
from uuid import UUID, uuid4

class Entity(ABC):
    """Base entity for all domain models."""
    
    def __init__(self, id: UUID = None):
        self._id = id or uuid4()
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
    
    @property
    def id(self) -> UUID:
        return self._id
        
    @property
    def created_at(self) -> datetime:
        return self._created_at
        
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def update_timestamp(self):
        """Update the last modified timestamp."""
        self._updated_at = datetime.utcnow()