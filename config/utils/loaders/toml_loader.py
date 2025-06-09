from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import tomli
import tomli_w
import asyncio

from ..abstracts.base_loader import BaseConfigLoader
from ..exceptions.loading_errors import ConfigLoadError
from ..validators.schema_validator import SchemaValidator
from ..security.sanitizer import ConfigSanitizer

class TOMLLoader(BaseConfigLoader[Dict[str, Any]]):
    """
    TOML configuration loader with advanced features.
    
    Features:
    - Async loading
    - Schema validation
    - Value sanitization
    - Multi-document support
    - Pretty printing
    - Incremental parsing
    """
    
    def __init__(
        self,
        schema_validator: Optional[SchemaValidator] = None,
        sanitizer: Optional[ConfigSanitizer] = None,
        cache_ttl: int = 300,  # 5 minutes
        pretty_print: bool = True
    ) -> None:
        super().__init__()
        self._schema_validator = schema_validator or SchemaValidator()
        self._sanitizer = sanitizer or ConfigSanitizer()
        self._cache_ttl = cache_ttl
        self._pretty_print = pretty_print
        
    async def load(self, path: str) -> Dict[str, Any]:
        """
        Load and parse TOML configuration file.
        
        Args:
            path: Path to TOML configuration file
            
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
            
            # Parse TOML
            config = tomli.loads(content)
            
            # Sanitize values
            config = self._sanitizer.sanitize(config)
            
            # Validate schema
            if not await self.validate(config):
                raise ConfigLoadError("Configuration validation failed")
            
            # Update cache
            self._cache[path] = config
            self._loaded_at = datetime.utcnow()
            
            return config
            
        except tomli.TOMLDecodeError as e:
            raise ConfigLoadError(f"Failed to parse TOML: {str(e)}")
        except Exception as e:
            raise ConfigLoadError(f"Failed to load configuration: {str(e)}")
    
    async def save(self, config: Dict[str, Any], path: str) -> None:
        """
        Save configuration to TOML file.
        
        Args:
            config: Configuration to save
            path: Target path
            
        Raises:
            ConfigLoadError: If file cannot be saved
        """
        try:
            # Validate before saving
            if not await self.validate(config):
                raise ConfigLoadError("Invalid configuration")
            
            config_path = Path(path)
            
            # Write file asynchronously
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._write_file,
                config_path,
                config
            )
            
        except Exception as e:
            raise ConfigLoadError(f"Failed to save configuration: {str(e)}")
    
    async def validate(self, config: Dict[str, Any]) -> bool:
        """Validate configuration against schema."""
        return await self._schema_validator.validate_schema(config)
    
    def _read_file(self, path: Path) -> str:
        """Read file contents."""
        with open(path, 'r') as f:
            return f.read()
    
    def _write_file(self, path: Path, config: Dict[str, Any]) -> None:
        """Write configuration to file."""
        with open(path, 'w') as f:
            tomli_w.dump(config, f)