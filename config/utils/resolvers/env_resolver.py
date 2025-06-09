from typing import Any, Dict, Optional, Set
import os
import re
from datetime import datetime

from ..exceptions.loading_errors import ConfigLoadError

class EnvResolver:
    """
    Environment variable resolver with advanced features.
    
    Features:
    - Variable interpolation
    - Default values
    - Type conversion
    - Prefix handling
    - Required variables
    """
    
    def __init__(
        self,
        prefix: str = '',
        case_sensitive: bool = False,
        required_vars: Optional[Set[str]] = None
    ) -> None:
        self.prefix = prefix
        self.case_sensitive = case_sensitive
        self.required_vars = required_vars or set()
        self._pattern = re.compile(r'\${([^}^{]+)}')
        self._resolved_cache: Dict[str, Any] = {}
        
    async def resolve(
        self,
        name: str,
        default: Any = None,
        var_type: Any = str
    ) -> Any:
        """
        Resolve environment variable.
        
        Args:
            name: Variable name
            default: Default value
            var_type: Type to convert to
            
        Returns:
            Resolved value
        """
        try:
            # Apply prefix
            full_name = f"{self.prefix}{name}" if self.prefix else name
            
            # Adjust case
            if not self.case_sensitive:
                full_name = full_name.upper()
            
            # Check if required
            if full_name in self.required_vars and full_name not in os.environ:
                raise ConfigLoadError(
                    f"Required environment variable not set: {full_name}"
                )
            
            # Get value
            value = os.environ.get(full_name)
            
            # Handle default
            if value is None:
                return default
            
            # Interpolate variables
            value = self._interpolate_vars(value)
            
            # Convert type
            return self._convert_type(value, var_type)
            
        except Exception as e:
            raise ConfigLoadError(
                f"Environment variable resolution failed: {str(e)}"
            )
    
    async def resolve_all(
        self,
        mapping: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve multiple environment variables.
        
        Args:
            mapping: Dictionary of variable names to default values
            
        Returns:
            Dictionary of resolved values
        """
        result = {}
        for name, config in mapping.items():
            default = config.get('default')
            var_type = config.get('type', str)
            value = await self.resolve(name, default, var_type)
            result[name] = value
        return result
    
    def _interpolate_vars(self, value: str) -> str:
        """
        Interpolate environment variables in string.
        
        Args:
            value: String to interpolate
            
        Returns:
            Interpolated string
        """
        matches = self._pattern.findall(value)
        if not matches:
            return value
            
        for var in matches:
            env_value = os.environ.get(var, '')
            value = value.replace(f'${{{var}}}', env_value)
            
        return value
    
    def _convert_type(self, value: str, var_type: Any) -> Any:
        """
        Convert string value to specified type.
        
        Args:
            value: String value
            var_type: Type to convert to
            
        Returns:
            Converted value
        """
        if var_type == bool:
            return value.lower() in ('true', 'yes', '1', 'on')
        elif var_type == list:
            return [v.strip() for v in value.split(',')]
        elif var_type == dict:
            pairs = [p.strip() for p in value.split(',')]
            return dict(p.split(':') for p in pairs)
        else:
            return var_type(value)