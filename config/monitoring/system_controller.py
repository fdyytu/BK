
import psutil
from typing import Dict, Any
from datetime import datetime
import platform
import os

class SystemCollector:
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics"""
        cpu_metrics = self._collect_cpu_metrics()
        memory_metrics = self._collect_memory_metrics()
        disk_metrics = self._collect_disk_metrics()
        network_metrics = self._collect_network_metrics()
        
        return {
            "timestamp_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "system": {
                "hostname": platform.node(),
                "os": platform.system(),
                "platform": platform.platform(),
                "cpu": cpu_metrics,
                "memory": memory_metrics,
                "disk": disk_metrics,
                "network": network_metrics
            }
        }

    def _collect_cpu_metrics(self) -> Dict[str, float]:
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "load_avg_1": os.getloadavg()[0],
            "load_avg_5": os.getloadavg()[1],
            "load_avg_15": os.getloadavg()[2],
            "core_count": psutil.cpu_count()
        }

    def _collect_memory_metrics(self) -> Dict[str, float]:
        mem = psutil.virtual_memory()
        return {
            "total_gb": mem.total / (1024 ** 3),
            "used_gb": mem.used / (1024 ** 3),
            "free_gb": mem.free / (1024 ** 3),
            "usage_percent": mem.percent
        }

    def _collect_disk_metrics(self) -> Dict[str, float]:
        disk = psutil.disk_usage('/')
        return {
            "total_gb": disk.total / (1024 ** 3),
            "used_gb": disk.used / (1024 ** 3),
            "free_gb": disk.free / (1024 ** 3),
            "usage_percent": disk.percent
        }

    def _collect_network_metrics(self) -> Dict[str, float]:
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "error_in": net_io.errin,
            "error_out": net_io.errout
        }