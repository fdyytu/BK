import sys
import traceback
from typing import Dict, Any, Optional
from datetime import datetime

class ErrorLogger:
    def __init__(self):
        self.logger = logging.getLogger('error')

    def log_exception(
        self,
        exc: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> None:
        error_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'error_type': exc.__class__.__name__,
            'error_message': str(exc),
            'traceback': traceback.format_exc(),
            'user_id': user_id,
            'context': context or {},
            'python_version': sys.version,
        }
        
        self.logger.error('Unhandled exception', extra=error_data)