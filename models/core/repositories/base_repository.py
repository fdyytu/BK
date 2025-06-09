from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID
from models.core.base.entity import Entity

T = TypeVar('T', bound=Entity)

class Repository(Generic[T], ABC):
    """Base repository interface."""
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        pass
        
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
        
    @abstractmethod 
    async def delete(self, id: UUID) -> bool:
        pass