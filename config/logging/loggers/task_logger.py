from typing import Any, Optional
from datetime import datetime

class TaskLogger:
    def __init__(self):
        self.logger = logging.getLogger('task')

    def log_task_execution(
        self,
        task_id: str,
        task_name: str,
        status: str,
        execution_time: float,
        **kwargs: Any
    ) -> None:
        """Log background task execution"""
        task_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'task_id': task_id,
            'task_name': task_name,
            'status': status,
            'execution_time_ms': round(execution_time * 1000, 2),
            **kwargs
        }
        
        self.logger.info('Task execution', extra=task_data)