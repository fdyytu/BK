from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class Entity(ABC):
    """Base entity for all domain models."""
    
    def __init__(self, id: UUID = None):
        self._id = id or uuid4()
        self._created_at = datetime.utcnow()
        self._updated_at = self._created_at
        
    @property
    def id(self) -> UUID:
        return self._id

class AggregateRoot(Entity):
    """Base class for aggregate roots."""
    pass