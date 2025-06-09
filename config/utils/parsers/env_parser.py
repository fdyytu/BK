from typing import Any, Dict, Optional, Union
from pathlib import Path
import os
import re
from datetime import datetime, timedelta

from ..abstracts.base_parser import BaseParser
from ..exceptions.validation_errors import ConfigValidationError

class EnvParser(BaseParser[str, Dict[str, Any]]):
    """
    Environment variable parser with advanced features.
    
    Features:
    - Complex value parsing
    - Type inference
    - Variable interpolation
    - Default values
    - Nested structures
    """
    
    def __init__(
        self,
        prefix: str = '',
        case_sensitive: bool = False,
        expand_vars: bool = True
    ) -> None:
        super().__init__()
        self.prefix = prefix
        self.case_sensitive = case_sensitive
        self.expand_vars = expand_vars
        self._pattern = re.compile(r'\${([^}^{]+)}')
    
    async def parse(self, data: str) -> Dict[str, Any]:
        """
        Parse environment variable string.
        
        Args:
            data: Environment variable string
            
        Returns:
            Parsed configuration dictionary
        """
        try:
            # Split into lines
            lines = data.strip().split('\n')
            config: Dict[str, Any] = {}
            
            for line in lines:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse key-value pair
                key, value = self._parse_line(line)
                
                # Apply prefix filter
                if self.prefix and not key.startswith(self.prefix):
                    continue
                
                # Remove prefix if exists
                if self.prefix:
                    key = key[len(self.prefix):]
                
                # Convert case if needed
                if not self.case_sensitive:
                    key = key.lower()
                
                # Parse value
                parsed_value = self._parse_value(value)
                
                # Handle nested keys
                self._set_nested_value(config, key, parsed_value)
            
            return config
            
        except Exception as e:
            raise ConfigValidationError(f"Failed to parse environment: {str(e)}")
    
    async def serialize(self, data: Dict[str, Any]) -> str:
        """
        Serialize configuration to environment format.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            Environment variable string
        """
        try:
            lines = []
            
            def _flatten_dict(d: Dict[str, Any], prefix: str = '') -> None:
                for key, value in d.items():
                    full_key = f"{prefix}{key}" if prefix else key
                    
                    if isinstance(value, dict):
                        _flatten_dict(value, f"{full_key}_")
                    else:
                        # Add prefix if configured
                        if self.prefix:
                            full_key = f"{self.prefix}{full_key}"
                        
                        # Convert case if needed
                        if not self.case_sensitive:
                            full_key = full_key.upper()
                        
                        # Serialize value
                        serialized_value = self._serialize_value(value)
                        lines.append(f"{full_key}={serialized_value}")
            
            _flatten_dict(data)
            return '\n'.join(sorted(lines))
            
        except Exception as e:
            raise ConfigValidationError(f"Failed to serialize environment: {str(e)}")
    
    def _parse_line(self, line: str) -> tuple[str, str]:
        """Parse single environment variable line."""
        try:
            key, value = line.split('=', 1)
            return key.strip(), value.strip().strip("'").strip('"')
        except ValueError:
            raise ValueError(f"Invalid environment variable line: {line}")
    
    def _parse_value(self, value: str) -> Any:
        """Parse environment variable value."""
        # Expand variables if enabled
        if self.expand_vars:
            value = self._expand_variables(value)
        
        # Try to infer type
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        elif value.isdigit():
            return int(value)
        elif value.replace('.', '').isdigit() and value.count('.') == 1:
            return float(value)
        elif value.startswith('[') and value.endswith(']'):
            try:
                import json
                return json.loads(value)
            except:
                return value
        elif value.lower() in ('none', 'null'):
            return None
        
        return value
    
    def _expand_variables(self, value: str) -> str:
        """Expand environment variables in value."""
        if not self.expand_vars:
            return value
            
        matches = self._pattern.findall(value)
        if not matches:
            return value
            
        for var in matches:
            env_value = os.environ.get(var, '')
            value = value.replace(f'${{{var}}}', env_value)
            
        return value
    
    def _set_nested_value(
        self,
        config: Dict[str, Any],
        key: str,
        value: Any
    ) -> None:
        """Set value in nested dictionary structure."""
        parts = key.split('_')
        
        current = config
        for part in parts[:-1]:
            current = current.setdefault(part, {})
            
        current[parts[-1]] = value
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize value to string."""
        if isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (list, dict)):
            import json
            return json.dumps(value)
        elif value is None:
            return 'null'
        else:
            return str(value)