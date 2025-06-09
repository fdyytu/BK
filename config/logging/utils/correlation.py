from contextvars import ContextVar
from typing import Optional
from uuid import uuid4

class CorrelationID:
    _correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')

    @classmethod
    def get(cls) -> str:
        return cls._correlation_id.get()

    @classmethod
    def set(cls, correlation_id: Optional[str] = None) -> None:
        cls._correlation_id.set(correlation_id or str(uuid4()))

    @classmethod
    def reset(cls) -> None:
        cls._correlation_id.set('')