from datetime import datetime
from typing import Dict, Any, Optional
from models.events.event_base import EventBase

class DomainEvent(EventBase):
    """Enhanced domain event implementation."""
    
    def __init__(self, name: str, payload: Dict[str, Any], user_id: Optional[int] = None):
        super().__init__()
        self.name = name
        self.payload = payload
        self.user_id = user_id
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert domain event to dictionary."""
        base_dict = super().to_dict()
        return {
            **base_dict,
            'name': self.name,
            'payload': self.payload,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainEvent':
        """Create domain event from dictionary."""
        event = cls(
            name=data['name'],
            payload=data['payload'],
            user_id=data.get('user_id')
        )
        event.event_id = data['event_id']
        event.timestamp = datetime.fromisoformat(data['timestamp'])
        event.processed = data['processed']
        return event