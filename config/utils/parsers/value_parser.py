from typing import Any, Dict, Optional, Type, TypeVar, Union
from datetime import datetime, timedelta
import re
from decimal import Decimal
import json

from ..abstracts.base_parser import BaseParser
from ..exceptions.validation_errors import ConfigValidationError

T = TypeVar('T')

class ValueParser(BaseParser[str, Any]):
    """
    Advanced value parser with support for multiple data types.
    
    Features:
    - Type inference
    - Custom type conversion
    - Format validation
    - Range checking
    - Unit conversion
    - Error handling
    """
    
    def __init__(
        self,
        default_type: Optional[Type] = None,
        strict_mode: bool = True,
        custom_parsers: Optional[Dict[str, callable]] = None
    ) -> None:
        super().__init__()
        self.default_type = default_type
        self.strict_mode = strict_mode
        self._custom_parsers = custom_parsers or {}
        self._setup_default_parsers()
    
    async def parse(self, data: str) -> Any:
        """
        Parse string value into appropriate type.
        
        Args:
            data: String value to parse
            
        Returns:
            Parsed value
            
        Raises:
            ConfigValidationError: If parsing fails
        """
        try:
            # Check for custom parser
            if ':' in data:
                type_hint, value = data.split(':', 1)
                if type_hint in self._custom_parsers:
                    return self._custom_parsers[type_hint](value)
            
            # Try default type if specified
            if self.default_type:
                try:
                    return self._convert_value(data, self.default_type)
                except:
                    if self.strict_mode:
                        raise
            
            # Try to infer type
            return self._infer_type(data)
            
        except Exception as e:
            raise ConfigValidationError(f"Failed to parse value: {str(e)}")
    
    async def serialize(self, data: Any) -> str:
        """
        Serialize value to string.
        
        Args:
            data: Value to serialize
            
        Returns:
            Serialized string
        """
        try:
            # Handle None
            if data is None:
                return 'null'
            
            # Handle basic types
            if isinstance(data, (str, int, float, bool)):
                return str(data)
            
            # Handle datetime
            if isinstance(data, datetime):
                return data.isoformat()
            
            # Handle timedelta
            if isinstance(data, timedelta):
                return f"duration:{data.total_seconds()}"
            
            # Handle Decimal
            if isinstance(data, Decimal):
                return f"decimal:{str(data)}"
            
            # Handle complex types
            if isinstance(data, (list, dict)):
                return json.dumps(data)
            
            # Default
            return str(data)
            
        except Exception as e:
            raise ConfigValidationError(f"Failed to serialize value: {str(e)}")
    
    def _setup_default_parsers(self) -> None:
        """Setup default type parsers."""
        self._custom_parsers.update({
            'int': int,
            'float': float,
            'bool': self._parse_bool,
            'str': str,
            'datetime': self._parse_datetime,
            'duration': self._parse_duration,
            'decimal': self._parse_decimal,
            'list': self._parse_list,
            'dict': self._parse_dict
        })
    
    def _infer_type(self, value: str) -> Any:
        """Infer and convert value type."""
        # Try boolean
        if value.lower() in ('true', 'false'):
            return self._parse_bool(value)
        
        # Try integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Try JSON
        try:
            return json.loads(value)
        except ValueError:
            pass
        
        # Default to string
        return value
    
    def _convert_value(self, value: str, target_type: Type[T]) -> T:
        """Convert value to target type."""
        if target_type == bool:
            return self._parse_bool(value)
        return target_type(value)
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean value."""
        return value.lower() in ('true', 'yes', '1', 'on')
    
    def _parse_datetime(self, value: str) -> datetime:
        """Parse datetime value."""
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            # Try common formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Invalid datetime format: {value}")
    
    def _parse_duration(self, value: str) -> timedelta:
        """Parse duration value."""
        # Parse format like "1h30m", "2d", "30s"
        pattern = re.compile(r'(\d+)([dhms])')
        matches = pattern.findall(value)
        if not matches:
            # Try seconds
            return timedelta(seconds=float(value))
        
        total_seconds = 0
        for amount, unit in matches:
            amount = int(amount)
            if unit == 'd':
                total_seconds += amount * 86400
            elif unit == 'h':
                total_seconds += amount * 3600
            elif unit == 'm':
                total_seconds += amount * 60
            elif unit == 's':
                total_seconds += amount
                
        return timedelta(seconds=total_seconds)
    
    def _parse_decimal(self, value: str) -> Decimal:
        """Parse decimal value."""
        return Decimal(value)
    
    def _parse_list(self, value: str) -> list:
        """Parse list value."""
        return json.loads(value)
    
    def _parse_dict(self, value: str) -> dict:
        """Parse dictionary value."""
        return json.loads(value)