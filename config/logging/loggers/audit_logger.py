from typing import Dict, Any, Optional
from datetime import datetime
import json

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('audit')

    def log_data_access(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        changes: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """Log data access for compliance and audit purposes"""
        audit_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': user_id,
            'action': action,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'changes': changes,
            'ip_address': kwargs.get('ip_address'),
            'user_agent': kwargs.get('user_agent'),
            'session_id': kwargs.get('session_id')
        }
        
        self.logger.info('Data access audit', extra=audit_data)

    def log_compliance_event(
        self,
        event_type: str,
        description: str,
        user_id: Optional[str] = None,
        regulation: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Log compliance-related events"""
        compliance_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'event_type': event_type,
            'description': description,
            'user_id': user_id,
            'regulation': regulation,
            **kwargs
        }
        
        self.logger.info('Compliance event', extra=compliance_data)