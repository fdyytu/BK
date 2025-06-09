from typing import Any, Optional
from datetime import datetime

class CacheLogger:
    def __init__(self):
        self.logger = logging.getLogger('cache')

    def log_cache_operation(
        self,
        operation: str,
        key: str,
        success: bool,
        execution_time: float,
        **kwargs: Any
    ) -> None:
        """Log cache operations"""
        cache_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'key': key,
            'success': success,
            'execution_time_ms': round(execution_time * 1000, 2),
            **kwargs
        }
        
        self.logger.info('Cache operation', extra=cache_data)