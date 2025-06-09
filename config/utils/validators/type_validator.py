from typing import Any, Dict, Optional, Type, Union
from datetime import datetime
import re

from ..abstracts.base_validator import BaseValidator
from ..exceptions.validation_errors import ConfigValidationError

class TypeValidator(BaseValidator[Dict[str, Any]]):
    """
    Advanced type validator with support for:
    - Complex type checking
    - Custom type definitions
    - Type coercion
    - Nested type validation
    """
    
    def __init__(self, strict_mode: bool = True) -> None:
        super().__init__()
        self.strict_mode = strict_mode
        self._type_mapping: Dict[str, Type] = {
            'string': str,
            'integer': int,
            'float': float,
            'boolean': bool,
            'list': list,
            'dict': dict,
            'datetime': datetime
        }
        self._custom_types: Dict[str, callable] = {}
    
    async def validate(
        self,
        data: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> bool:
        """
        Validate types in configuration data.
        
        Args:
            data: Data to validate
            context: Optional validation context
            
        Returns:
            True if valid
            
        Raises:
            ConfigValidationError: If validation fails in strict mode
        """
        try:
            for key, value in data.items():
                if isinstance(value, dict) and '_type' in value:
                    expected_type = value['_type']
                    actual_value = value.get('value')
                    
                    if expected_type in self._custom_types:
                        if not self._custom_types[expected_type](actual_value):
                            self._add_type_error(key, expected_type, actual_value)
                    elif expected_type in self._type_mapping:
                        if not isinstance(actual_value, self._type_mapping[expected_type]):
                            self._add_type_error(key, expected_type, actual_value)
                    else:
                        self._add_type_error(key, expected_type, actual_value,
                                           "Unknown type")
            
            if self._errors and self.strict_mode:
                raise ConfigValidationError(
                    "Type validation failed",
                    details={'errors': self._errors}
                )
            
            return len(self._errors) == 0
            
        except Exception as e:
            if self.strict_mode:
                raise
            self.add_error({
                'type': 'validation_error',
                'message': str(e)
            })
            return False
    
    async def get_validation_rules(self) -> Dict[str, Any]:
        """Get current validation rules."""
        return {
            'type_mapping': self._type_mapping,
            'custom_types': list(self._custom_types.keys())
        }
    
    def add_custom_type(
        self,
        type_name: str,
        validator: callable
    ) -> None:
        """
        Add custom type validator.
        
        Args:
            type_name: Name of custom type
            validator: Validation function
        """
        self._custom_types[type_name] = validator
    
    def _add_type_error(
        self,
        key: str,
        expected_type: str,
        actual_value: Any,
        message: Optional[str] = None
    ) -> None:
        """Add type validation error."""
        self.add_error({
            'type': 'type_error',
            'key': key,
            'expected_type': expected_type,
            'actual_type': type(actual_value).__name__,
            'message': message or f"Invalid type for '{key}'"
        })