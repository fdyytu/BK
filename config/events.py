from typing import Dict, Any, Callable, List
from enum import Enum
from dataclasses import dataclass

class EventTypes(str, Enum):
    # User Events
    USER_REGISTERED = "user.registered"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    
    # Payment Events
    PAYMENT_CREATED = "payment.created"
    PAYMENT_COMPLETED = "payment.completed"
    PAYMENT_FAILED = "payment.failed"
    
    # Order Events
    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    ORDER_COMPLETED = "order.completed"

@dataclass
class EventConfig:
    type: EventTypes
    handlers: List[Callable]
    retry_count: int = 3
    timeout: int = 30
    async_execution: bool = True

class EventBusConfig:
    """Event bus configuration."""
    
    def __init__(self):
        self.events: Dict[str, EventConfig] = {}
        self.initialize_events()
    
    def initialize_events(self):
        """Initialize default event configurations."""
        for event_type in EventTypes:
            self.events[event_type] = EventConfig(
                type=event_type,
                handlers=[],
                retry_count=3,
                timeout=30,
                async_execution=True
            )
    
    def register_handler(self, event_type: EventTypes, handler: Callable):
        """Register event handler."""
        if event_type in self.events:
            self.events[event_type].handlers.append(handler)
    
    def get_handlers(self, event_type: EventTypes) -> List[Callable]:
        """Get all handlers for an event type."""
        return self.events[event_type].handlers if event_type in self.events else []