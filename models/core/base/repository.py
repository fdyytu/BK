from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID
from contextlib import AbstractContextManager
from .entity import Entity

T = TypeVar('T', bound=Entity)

class Repository(Generic[T], ABC):
    """Base repository interface."""
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Get entity by ID."""
        pass
        
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save (create or update) entity."""
        pass
        
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Delete entity by ID."""
        pass
        
    @abstractmethod
    def unit_of_work(self) -> AbstractContextManager:
        """Get unit of work context manager."""
        pass