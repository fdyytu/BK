from typing import Dict, Any, Optional
from pathlib import Path
import json
import asyncio
from datetime import datetime

from ..abstracts.base_loader import BaseConfigLoader
from ..exceptions.loading_errors import ConfigLoadError
from ..validators.schema_validator import SchemaValidator
from ..security.sanitizer import ConfigSanitizer

class JSONLoader(BaseConfigLoader[Dict[str, Any]]):
    """
    JSON configuration loader with advanced features.
    
    Features:
    - Async file reading
    - Schema validation
    - Value sanitization
    - Caching with TTL
    - JSON5 support
    """
    
    def __init__(
        self,
        schema_validator: Optional[SchemaValidator] = None,
        sanitizer: Optional[ConfigSanitizer] = None,
        cache_ttl: int = 300,  # 5 minutes
        support_json5: bool = True
    ) -> None:
        super().__init__()
        self._schema_validator = schema_validator or SchemaValidator()
        self._sanitizer = sanitizer or ConfigSanitizer()
        self._cache_ttl = cache_ttl
        self._support_json5 = support_json5
        
        if support_json5:
            try:
                import json5
                self._json_parser = json5
            except ImportError:
                self._json_parser = json
        else:
            self._json_parser = json
    
    async def load(self, path: str) -> Dict[str, Any]:
        """
        Load and parse JSON configuration file.
        
        Args:
            path: Path to JSON configuration file
            
        Returns:
            Parsed configuration dictionary
            
        Raises:
            ConfigLoadError: If file cannot be loaded or parsed
        """
        try:
            # Check cache first
            if path in self._cache:
                cache_time = self._loaded_at
                if cache_time and (datetime.utcnow() - cache_time).seconds < self._cache_ttl:
                    return self._cache[path]
            
            config_path = Path(path)
            if not config_path.exists():
                raise ConfigLoadError(f"Configuration file not found: {path}")
            
            # Read file asynchronously
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(
                None,
                self._read_file,
                config_path
            )
            
            # Parse JSON
            config = self._json_parser.loads(content)
            
            # Sanitize values
            config = self._sanitizer.sanitize(config)
            
            # Validate schema
            if not await self.validate(config):
                raise ConfigLoadError("Configuration validation failed")
            
            # Update cache
            self._cache[path] = config
            self._loaded_at = datetime.utcnow()
            
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            raise ConfigLoadError(f"Failed to load configuration: {str(e)}")
    
    async def validate(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
            
        Raises:
            ConfigValidationError: If validation fails
        """
        return await self._schema_validator.validate_schema(config)
    
    def _read_file(self, path: Path) -> str:
        """Read file contents."""
        with open(path, 'r') as f:
            return f.read()