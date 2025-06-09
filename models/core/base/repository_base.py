from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

T = TypeVar('T')

class RepositoryBase(Generic[T], ABC):
    """Base repository interface."""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add new entity."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> bool:
        """Update existing entity."""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete entity by ID."""
        pass
    
    @abstractmethod
    def exists(self, id: int) -> bool:
        """Check if entity exists."""
        pass