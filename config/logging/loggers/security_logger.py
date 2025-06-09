from typing import Dict, Any, Optional
from datetime import datetime

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')

    def log_auth_event(
        self,
        event_type: str,
        user_id: str,
        success: bool,
        ip_address: str,
        **kwargs: Any
    ) -> None:
        log_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'event_type': event_type,
            'user_id': user_id,
            'success': success,
            'ip_address': ip_address,
            **kwargs
        }
        
        self.logger.info(f'Authentication {event_type}', extra=log_data)

    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        user_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        log_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'event_type': event_type,
            'severity': severity,
            'description': description,
            'user_id': user_id,
            **kwargs
        }
        
        self.logger.warning('Security event detected', extra=log_data)