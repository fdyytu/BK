from abc import ABC
from typing import Generic, TypeVar
from .repository import Repository
from .entity import Entity
from .exceptions import BusinessError

T = TypeVar('T', bound=Entity)

class Service(Generic[T], ABC):
    """Base service with common functionality."""
    
    def __init__(self, repository: Repository[T]):
        self._repository = repository
        
    async def get_by_id(self, id: UUID) -> T:
        """Get entity by ID or raise error."""
        entity = await self._repository.get_by_id(id)
        if not entity:
            raise BusinessError(f"Entity with ID {id} not found")
        return entity
        
    async def save(self, entity: T) -> T:
        """Save entity with validation."""
        self._validate(entity)
        async with self._repository.unit_of_work():
            return await self._repository.save(entity)
            
    def _validate(self, entity: T) -> None:
        """Validate entity before save."""
        if not entity.is_valid():
            raise BusinessError("Invalid entity state")