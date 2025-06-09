from typing import Dict, Any
import time
import psutil
from datetime import datetime

class MetricsLogger:
    def __init__(self):
        self.logger = logging.getLogger('metrics')

    def log_system_metrics(self) -> None:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'network_connections': len(psutil.net_connections())
        }
        
        self.logger.info('System metrics', extra=metrics)

    def log_api_metrics(self, path: str, method: str, response_time: float, status_code: int) -> None:
        metrics = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'path': path,
            'method': method,
            'response_time_ms': round(response_time * 1000, 2),
            'status_code': status_code
        }
        
        self.logger.info('API metrics', extra=metrics)