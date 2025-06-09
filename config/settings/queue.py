from typing import Dict, Any, List
from pydantic import BaseModel
from enum import Enum
from datetime import timedelta
from .environment import EnvironmentSettings

class QueueProvider(str, Enum):
    REDIS = "redis"
    RABBITMQ = "rabbitmq"
    SQS = "sqs"

class QueuePriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskRetryPolicy(BaseModel):
    """Task retry configuration."""
    max_retries: int = 3
    retry_delays: List[int] = [5, 30, 300]  # seconds
    backoff_factor: float = 2.0
    max_backoff: int = 3600  # 1 hour

class QueueSettings(BaseModel):
    """Queue/Worker configuration settings."""
    
    enabled: bool = True
    provider: QueueProvider = QueueProvider.REDIS
    
    # Queue Configuration
    queues: Dict[str, Dict[str, Any]] = {
        "default": {
            "priority": QueuePriority.MEDIUM,
            "max_concurrent": 10
        },
        "high": {
            "priority": QueuePriority.HIGH,
            "max_concurrent": 20
        },
        "low": {
            "priority": QueuePriority.LOW,
            "max_concurrent": 5
        }
    }
    
    # Worker Settings
    worker_concurrency: int = 4
    worker_prefetch_count: int = 10
    worker_log_level: str = "INFO"
    
    # Task Settings
    task_default_queue: str = "default"
    task_serializer: str = "json"
    task_compression: Optional[str] = "gzip"
    task_acks_late: bool = True
    
    # Result Backend
    result_backend: str = "redis"
    result_expires: timedelta = timedelta(days=1)
    
    # Retry Policy
    retry_policy: TaskRetryPolicy = TaskRetryPolicy()
    
    # Monitoring
    monitor_enabled: bool = True
    monitor_interval: int = 60
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "QueueSettings":
        """Create settings from environment."""
        return cls(
            enabled=env.get_env("QUEUE_ENABLED", "true").lower() == "true",
            provider=QueueProvider(env.get_env("QUEUE_PROVIDER", "redis")),
            worker_concurrency=int(env.get_env("WORKER_CONCURRENCY", "4"))
        )