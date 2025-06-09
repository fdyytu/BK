from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, Any
from .entity import Entity

T = TypeVar('T', bound=Entity)

class DataMapper(Generic[T], ABC):
    """Interface for mapping between entities and DTOs."""
    
    @abstractmethod
    def to_entity(self, data: Dict[str, Any]) -> T:
        """Map data to entity."""
        pass
        
    @abstractmethod
    def to_dict(self, entity: T) -> Dict[str, Any]:
        """Map entity to dictionary."""
        pass