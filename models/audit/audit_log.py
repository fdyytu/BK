from datetime import datetime
from typing import Dict, Any, Optional, List
from models.audit.audit_base import AuditEntry
from models.common.enums import Status

class AuditLog(AuditEntry):
    """Enhanced audit log implementation."""
    
    def __init__(self,
                 action: str,
                 user_id: int,
                 resource_type: str,
                 resource_id: str,
                 details: str = '',
                 status: Status = Status.ACTIVE):
        super().__init__(action, user_id, resource_type, resource_id, status)
        self.details = details
        self.ip_address: Optional[str] = None
        self.user_agent: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary."""
        base_dict = super().to_dict()
        return {
            **base_dict,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditLog':
        """Create audit log from dictionary."""
        log = cls(
            action=data['action'],
            user_id=data['user_id'],
            resource_type=data['resource_type'],
            resource_id=data['resource_id'],
            details=data.get('details', ''),
            status=Status(data['status'])
        )
        log.id = data.get('id')
        log.timestamp = datetime.fromisoformat(data['timestamp'])
        log.metadata = data.get('metadata', {})
        log.ip_address = data.get('ip_address')
        log.user_agent = data.get('user_agent')
        return log