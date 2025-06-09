from typing import Any

class Singleton:
    """Singleton pattern implementation"""
    
    _instances = {}
    
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.initialized = True