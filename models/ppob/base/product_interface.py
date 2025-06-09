from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class IProduct(ABC):
    """Product interface defining common behavior."""
    
    @abstractmethod
    def get_price(self) -> float:
        """Get product price."""
        pass
    
    @abstractmethod
    def get_details(self) -> Dict[str, Any]:
        """Get product details."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if product is available."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate product data."""
        pass