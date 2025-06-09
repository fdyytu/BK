from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar, List
from datetime import datetime

T = TypeVar('T')

class BaseValidator(ABC, Generic[T]):
    """
    Abstract base class for all validators.
    
    Provides interface and common functionality for validating
    configuration data with type safety and error tracking.
    """
    
    def __init__(self) -> None:
        self._errors: List[Dict[str, Any]] = []
        self._last_validation: Optional[datetime] = None
        
    @abstractmethod
    async def validate(self, data: T, context: Optional[Dict] = None) -> bool:
        """
        Validate the provided data.
        
        Args:
            data: Data to validate
            context: Optional validation context
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_validation_rules(self) -> Dict[str, Any]:
        """
        Get current validation rules.
        
        Returns:
            Dictionary of validation rules
        """
        pass
    
    def add_error(self, error: Dict[str, Any]) -> None:
        """Add validation error to error list."""
        self._errors.append({
            'timestamp': datetime.utcnow().isoformat(),
            **error
        })
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """Get all validation errors."""
        return self._errors
    
    def clear_errors(self) -> None:
        """Clear all validation errors."""
        self._errors.clear()
    
    def get_last_validation(self) -> Optional[datetime]:
        """Get timestamp of last validation."""
        return self._last_validation