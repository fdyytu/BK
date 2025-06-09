from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import threading

@dataclass
class CacheMetrics:
    hits: int = 0
    misses: int = 0
    keys: int = 0
    memory_usage: float = 0.0
    last_update: datetime = datetime.utcnow()

class MetricsCollector:
    """Collect and track cache metrics"""
    
    def __init__(self):
        self._metrics = CacheMetrics()
        self._lock = threading.Lock()
    
    def record_hit(self):
        with self._lock:
            self._metrics.hits += 1
            self._metrics.last_update = datetime.utcnow()
    
    def record_miss(self):
        with self._lock:
            self._metrics.misses += 1
            self._metrics.last_update = datetime.utcnow()
    
    def get_hit_ratio(self) -> float:
        total = self._metrics.hits + self._metrics.misses
        return self._metrics.hits / total if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'hits': self._metrics.hits,
            'misses': self._metrics.misses,
            'hit_ratio': self.get_hit_ratio(),
            'keys': self._metrics.keys,
            'memory_usage': self._metrics.memory_usage,
            'last_update': self._metrics.last_update.isoformat()
        }