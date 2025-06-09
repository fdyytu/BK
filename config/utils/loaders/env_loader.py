from typing import Dict, Any, Optional, Union
from pathlib import Path
import os
import re
from datetime import datetime

from ..abstracts.base_loader import BaseConfigLoader
from ..exceptions.loading_errors import ConfigLoadError
from ..security.sanitizer import ConfigSanitizer

class EnvLoader(BaseConfigLoader[Dict[str, Any]]):
    """
    Environment variables loader with advanced features.
    
    Features:
    - Multiple .env file support
    - Variable interpolation
    - Type casting
    - Nested structure support
    - Prefix filtering
    """
    
    def __init__(
        self,
        sanitizer: Optional[ConfigSanitizer] = None,
        prefix: str = '',
        auto_cast: bool = True,
        case_sensitive: bool = False
    ) -> None:
        super().__init__()
        self._sanitizer = sanitizer or ConfigSanitizer()
        self._prefix = prefix
        self._auto_cast = auto_cast
        self._case_sensitive = case_sensitive
        self._pattern = re.compile(r'\${([^}^{]+)}')
    
    async def load(self, path: str = '.env') -> Dict[str, Any]:
        """
        Load environment variables from file and/or OS.
        
        Args:
            path: Optional path to .env file
            
        Returns:
            Dictionary of environment variables
        """
        try:
            config: Dict[str, Any] = {}
            
            # Load from .env file if exists
            env_path = Path(path)
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            config[key.strip()] = value.strip().strip("'").strip('"')
            
            # Load from OS environment
            for key, value in os.environ.items():
                if self._prefix and not key.startswith(self._prefix):
                    continue
                    
                if not self._case_sensitive:
                    key = key.lower()
                
                config[key] = value
            
            # Process variables
            processed_config = self._process_variables(config)
            
            # Auto cast values if enabled
            if self._auto_cast:
                processed_config = self._auto_cast_values(processed_config)
            
            # Sanitize values
            processed_config = self._sanitizer.sanitize(processed_config)
            
            self._loaded_at = datetime.utcnow()
            return processed_config
            
        except Exception as e:
            raise ConfigLoadError(f"Failed to load environment variables: {str(e)}")
    
    async def validate(self, config: Dict[str, Any]) -> bool:
        """Validate environment variables."""
        # Basic validation - ensure all values are strings
        return all(isinstance(v, str) for v in config.values())
    
    def _process_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process variable interpolation."""
        processed: Dict[str, Any] = {}
        
        for key, value in config.items():
            if isinstance(value, str):
                # Replace ${VAR} with actual values
                matches = self._pattern.findall(value)
                if matches:
                    for var in matches:
                        var_value = config.get(var) or os.environ.get(var, '')
                        value = value.replace(f'${{{var}}}', var_value)
            
            processed[key] = value
            
        return processed
    
    def _auto_cast_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically cast values to appropriate types."""
        casted: Dict[str, Any] = {}
        
        for key, value in config.items():
            if isinstance(value, str):
                # Boolean
                if value.lower() in ('true', 'false'):
                    casted[key] = value.lower() == 'true'
                # Integer
                elif value.isdigit():
                    casted[key] = int(value)
                # Float
                elif value.replace('.', '').isdigit() and value.count('.') == 1:
                    casted[key] = float(value)
                # List
                elif value.startswith('[') and value.endswith(']'):
                    try:
                        import json
                        casted[key] = json.loads(value)
                    except:
                        casted[key] = value
                # None
                elif value.lower() in ('none', 'null'):
                    casted[key] = None
                else:
                    casted[key] = value
            else:
                casted[key] = value
                
        return casted