from typing import Generic, TypeVar, Optional, List, Type
from pydantic import BaseModel
from ..repository.database import DatabaseRepository
from ..events import EventBusConfig, EventTypes

T = TypeVar('T')
M = TypeVar('M', bound=BaseModel)

class BaseService(Generic[T, M]):
    """Base service layer implementation."""
    
    def __init__(
        self,
        repository: DatabaseRepository[T],
        event_bus: EventBusConfig,
        model: Type[M]
    ):
        self.repository = repository
        self.event_bus = event_bus
        self.model = model
    
    async def create(self, data: M) -> Optional[T]:
        """Create new entity and emit creation event."""
        instance = await self.repository.create(data.dict())
        if instance:
            await self.emit_event(EventTypes.CREATED, instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        return await self.repository.get_by_id(id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        return await self.repository.get_all(skip, limit)
    
    async def update(self, id: int, data: M) -> Optional[T]:
        """Update entity and emit update event."""
        instance = await self.repository.update(id, data.dict())
        if instance:
            await self.emit_event(EventTypes.UPDATED, instance)
        return instance
    
    async def delete(self, id: int) -> bool:
        """Delete entity and emit deletion event."""
        success = await self.repository.delete(id)
        if success:
            await self.emit_event(EventTypes.DELETED, {"id": id})
        return success
    
    async def emit_event(self, event_type: EventTypes, data: Any):
        """Emit event to event bus."""
        handlers = self.event_bus.get_handlers(event_type)
        for handler in handlers:
            await handler(data)