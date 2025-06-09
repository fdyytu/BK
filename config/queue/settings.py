from typing import Optional
from pydantic import BaseModel

class QueueSettings(BaseModel):
    broker: str = "redis"
    result_backend: Optional[str] = None
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: list = ["json"]
    enable_utc: bool = True
    timezone: str = "UTC"
    
    task_queues: dict = {
        "default": {"exchange": "default", "routing_key": "default"},
        "high": {"exchange": "high", "routing_key": "high"},
        "low": {"exchange": "low", "routing_key": "low"}
    }