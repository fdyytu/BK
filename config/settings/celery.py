from typing import Dict, Any, List
from pydantic import BaseModel, RedisDsn
from .environment import EnvironmentSettings

class CelerySettings(BaseModel):
    broker_url: RedisDsn = "redis://localhost:6379/1"
    result_backend: RedisDsn = "redis://localhost:6379/2"
    
    # Task settings
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: List[str] = ["json"]
    timezone: str = "UTC"
    enable_utc: bool = True
    
    # Queue settings
    task_queues: Dict[str, Dict[str, Any]] = {
        "default": {
            "exchange": "default",
            "routing_key": "default"
        },
        "high_priority": {
            "exchange": "high_priority",
            "routing_key": "high_priority"
        },
        "low_priority": {
            "exchange": "low_priority",
            "routing_key": "low_priority"
        }
    }
    
    # Task routing
    task_routes: Dict[str, Dict[str, str]] = {
        "tasks.high_priority.*": {"queue": "high_priority"},
        "tasks.low_priority.*": {"queue": "low_priority"}
    }
    
    # Retry settings
    task_retry_delays: List[int] = [3, 60, 300]  # 3s, 1m, 5m
    max_retries: int = 3
    
    # Rate limiting
    task_rate_limit: str = "100/s"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "CelerySettings":
        settings = cls()
        
        if env.is_production:
            settings.broker_url = "redis://prod-queue:6379/1"
            settings.result_backend = "redis://prod-queue:6379/2"
            settings.task_rate_limit = "1000/s"
            
        return settings