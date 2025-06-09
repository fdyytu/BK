from typing import Any, Optional
from datetime import datetime

class IntegrationLogger:
    def __init__(self):
        self.logger = logging.getLogger('integration')

    def log_external_request(
        self,
        service: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        **kwargs: Any
    ) -> None:
        """Log external service integration"""
        integration_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'service': service,
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_time_ms': round(response_time * 1000, 2),
            **kwargs
        }
        
        self.logger.info('External service request', extra=integration_data)