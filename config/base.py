from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseConfig(ABC):
    """Base configuration class that all config classes must inherit from"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        pass
        
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set config value"""
        pass
        
    @abstractmethod
    def load(self) -> None:
        """Load configuration"""
        pass
        
    @abstractmethod
    def validate(self) -> bool:
        """Validate configuration"""
        pass