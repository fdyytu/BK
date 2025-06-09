from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

class EventBase(ABC):
    """Base class for all events in the system."""
    
    def __init__(self):
        self.event_id: str = str(uuid4())
        self.timestamp: datetime = datetime.utcnow()
        self.processed: bool = False
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'processed': self.processed
        }