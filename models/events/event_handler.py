from abc import ABC, abstractmethod
from typing import Dict, Type, Callable, List
from models.events.domain_event import DomainEvent

class EventHandler(ABC):
    """Base class for event handlers."""
    
    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle the event."""
        pass

class EventBus:
    """Event bus for managing event handlers."""
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
    
    def register(self, event_name: str, handler: EventHandler) -> None:
        """Register an event handler."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
    
    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to all registered handlers."""
        if event.name in self._handlers:
            for handler in self._handlers[event.name]:
                await handler.handle(event)