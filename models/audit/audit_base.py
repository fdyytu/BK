from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
from models.common.enums import Status

class AuditEntry(ABC):
    """Base class for audit entries."""
    
    def __init__(self, 
                 action: str,
                 user_id: int,
                 resource_type: str,
                 resource_id: str,
                 status: Status = Status.ACTIVE):
        self.id: Optional[int] = None
        self.action = action
        self.user_id = user_id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.status = status
        self.timestamp = datetime.utcnow()
        self.metadata: Dict[str, Any] = {}
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit entry to dictionary."""
        return {
            'id': self.id,
            'action': self.action,
            'user_id': self.user_id,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'status': self.status.value,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }