from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar
from datetime import datetime

T = TypeVar('T')
U = TypeVar('U')

class BaseParser(ABC, Generic[T, U]):
    """
    Abstract base class for all parsers.
    
    Provides interface and common functionality for parsing
    configuration data with type safety and caching.
    """
    
    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
        self._last_parse: Optional[datetime] = None
        
    @abstractmethod
    async def parse(self, data: T) -> U:
        """
        Parse the provided data.
        
        Args:
            data: Data to parse
            
        Returns:
            Parsed data
        """
        pass
    
    @abstractmethod
    async def serialize(self, data: U) -> T:
        """
        Serialize data back to original format.
        
        Args:
            data: Data to serialize
            
        Returns:
            Serialized data
        """
        pass
    
    def clear_cache(self) -> None:
        """Clear parser cache."""
        self._cache.clear()
        self._last_parse = None