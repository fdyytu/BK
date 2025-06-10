"""
Enhanced Base Configuration System
Implements SOLID principles with comprehensive interfaces and abstractions
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Union, Type, Generic, TypeVar
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime

# Type definitions
T = TypeVar('T')
ConfigValue = Union[str, int, float, bool, Dict, List]

class ConfigSource(Enum):
    """Configuration source types"""
    ENVIRONMENT = "environment"
    FILE = "file"
    DATABASE = "database"
    REMOTE = "remote"
    MEMORY = "memory"

class ConfigPriority(Enum):
    """Configuration priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ConfigMetadata:
    """Configuration metadata"""
    source: ConfigSource
    priority: ConfigPriority
    created_at: datetime
    updated_at: Optional[datetime] = None
    version: str = "1.0.0"
    encrypted: bool = False
    cached: bool = False

class IConfigValidator(ABC):
    """Interface for configuration validators"""
    
    @abstractmethod
    def validate(self, key: str, value: Any) -> bool:
        """Validate configuration value"""
        pass
    
    @abstractmethod
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        pass

class IConfigLoader(ABC):
    """Interface for configuration loaders"""
    
    @abstractmethod
    def load(self, source: str) -> Dict[str, Any]:
        """Load configuration from source"""
        pass
    
    @abstractmethod
    def supports_source(self, source: ConfigSource) -> bool:
        """Check if loader supports source type"""
        pass

class IConfigSerializer(ABC):
    """Interface for configuration serializers"""
    
    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> str:
        """Serialize configuration data"""
        pass
    
    @abstractmethod
    def deserialize(self, data: str) -> Dict[str, Any]:
        """Deserialize configuration data"""
        pass

class IConfigEncryption(ABC):
    """Interface for configuration encryption"""
    
    @abstractmethod
    def encrypt(self, value: str) -> str:
        """Encrypt configuration value"""
        pass
    
    @abstractmethod
    def decrypt(self, encrypted_value: str) -> str:
        """Decrypt configuration value"""
        pass

class IConfigCache(ABC):
    """Interface for configuration caching"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get cached configuration value"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached configuration value"""
        pass
    
    @abstractmethod
    def invalidate(self, key: str) -> None:
        """Invalidate cached configuration"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all cached configurations"""
        pass

class IConfigObserver(ABC):
    """Interface for configuration change observers"""
    
    @abstractmethod
    def on_config_changed(self, key: str, old_value: Any, new_value: Any) -> None:
        """Handle configuration change event"""
        pass

class ConfigException(Exception):
    """Base configuration exception"""
    pass

class ConfigValidationError(ConfigException):
    """Configuration validation error"""
    pass

class ConfigLoadError(ConfigException):
    """Configuration load error"""
    pass

class ConfigNotFoundError(ConfigException):
    """Configuration not found error"""
    pass

class BaseConfig(ABC):
    """
    Enhanced base configuration class implementing SOLID principles
    
    Single Responsibility: Manages configuration data
    Open/Closed: Extensible through interfaces
    Liskov Substitution: All implementations are interchangeable
    Interface Segregation: Multiple focused interfaces
    Dependency Inversion: Depends on abstractions
    """
    
    def __init__(
        self,
        validator: Optional[IConfigValidator] = None,
        loader: Optional[IConfigLoader] = None,
        serializer: Optional[IConfigSerializer] = None,
        encryption: Optional[IConfigEncryption] = None,
        cache: Optional[IConfigCache] = None,
        logger: Optional[logging.Logger] = None
    ):
        self._data: Dict[str, Any] = {}
        self._metadata: Dict[str, ConfigMetadata] = {}
        self._observers: List[IConfigObserver] = []
        
        # Dependency injection
        self._validator = validator
        self._loader = loader
        self._serializer = serializer
        self._encryption = encryption
        self._cache = cache
        self._logger = logger or logging.getLogger(__name__)
        
        # Configuration state
        self._loaded = False
        self._validated = False
        self._readonly = False
    
    # Core abstract methods
    @abstractmethod
    def get_config_name(self) -> str:
        """Get configuration name"""
        pass
    
    @abstractmethod
    def get_default_values(self) -> Dict[str, Any]:
        """Get default configuration values"""
        pass
    
    @abstractmethod
    def get_required_keys(self) -> List[str]:
        """Get required configuration keys"""
        pass
    
    # Configuration management
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with caching support"""
        try:
            # Check cache first
            if self._cache:
                cached_value = self._cache.get(key)
                if cached_value is not None:
                    return cached_value
            
            # Get from data
            value = self._get_nested_value(key, default)
            
            # Decrypt if needed
            if self._is_encrypted(key) and self._encryption:
                value = self._encryption.decrypt(str(value))
            
            # Cache the value
            if self._cache and value is not None:
                self._cache.set(key, value)
            
            return value
            
        except Exception as e:
            self._logger.error(f"Error getting config key '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any, metadata: Optional[ConfigMetadata] = None) -> None:
        """Set configuration value with validation and encryption"""
        if self._readonly:
            raise ConfigException(f"Configuration is readonly, cannot set '{key}'")
        
        try:
            # Validate value
            if self._validator and not self._validator.validate(key, value):
                errors = self._validator.get_validation_errors()
                raise ConfigValidationError(f"Validation failed for '{key}': {errors}")
            
            # Get old value for observers
            old_value = self.get(key)
            
            # Encrypt if needed
            if self._should_encrypt(key) and self._encryption:
                value = self._encryption.encrypt(str(value))
            
            # Set value
            self._set_nested_value(key, value)
            
            # Set metadata
            if metadata:
                self._metadata[key] = metadata
            else:
                self._metadata[key] = ConfigMetadata(
                    source=ConfigSource.MEMORY,
                    priority=ConfigPriority.MEDIUM,
                    created_at=datetime.now()
                )
            
            # Invalidate cache
            if self._cache:
                self._cache.invalidate(key)
            
            # Notify observers
            self._notify_observers(key, old_value, value)
            
            self._logger.debug(f"Set config key '{key}' with value type: {type(value)}")
            
        except Exception as e:
            self._logger.error(f"Error setting config key '{key}': {e}")
            raise
    
    def load_defaults(self) -> None:
        """Load only default configuration values"""
        try:
            defaults = self.get_default_values()
            for key, value in defaults.items():
                if key not in self._data:
                    self._data[key] = value
                    self._metadata[key] = ConfigMetadata(
                        source=ConfigSource.MEMORY,
                        priority=ConfigPriority.LOW,
                        created_at=datetime.now()
                    )
            
            self._loaded = True
            self._logger.debug(f"Default values loaded for '{self.get_config_name()}'")
            
        except Exception as e:
            self._logger.error(f"Error loading defaults: {e}")
            raise ConfigLoadError(f"Failed to load defaults: {e}")
    
    def load(self, source: Optional[str] = None) -> None:
        """Load configuration from source"""
        try:
            if self._loader and source:
                data = self._loader.load(source)
                self._merge_data(data)
            
            # Load defaults for missing keys
            defaults = self.get_default_values()
            for key, value in defaults.items():
                if key not in self._data:
                    self.set(key, value, ConfigMetadata(
                        source=ConfigSource.MEMORY,
                        priority=ConfigPriority.LOW,
                        created_at=datetime.now()
                    ))
            
            self._loaded = True
            self._logger.info(f"Configuration '{self.get_config_name()}' loaded successfully")
            
        except Exception as e:
            self._logger.error(f"Error loading configuration: {e}")
            raise ConfigLoadError(f"Failed to load configuration: {e}")
    
    def validate(self) -> bool:
        """Validate entire configuration"""
        self._validation_errors = []
        
        try:
            # Check required keys
            required_keys = self.get_required_keys()
            missing_keys = [key for key in required_keys if key not in self._data]
            
            if missing_keys:
                self._validation_errors.append(f"Missing required keys: {missing_keys}")
            
            # Validate with validator if available
            if self._validator:
                for key, value in self._data.items():
                    if not self._validator.validate(key, value):
                        errors = self._validator.get_validation_errors()
                        self._validation_errors.extend([f"Key '{key}': {error}" for error in errors])
            
            if not self._validation_errors:
                self._validated = True
                self._logger.debug(f"Configuration '{self.get_config_name()}' validated successfully")
                return True
            else:
                self._validated = False
                self._logger.error(f"Configuration validation failed: {self._validation_errors}")
                return False
            
        except Exception as e:
            self._logger.error(f"Unexpected validation error: {e}")
            self._validation_errors.append(f"Validation error: {e}")
            self._validated = False
            return False
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors from last validation"""
        return getattr(self, '_validation_errors', [])
    
    # Advanced features
    def reload(self) -> None:
        """Reload configuration"""
        self._loaded = False
        self._validated = False
        if self._cache:
            self._cache.clear()
        self.load()
        self.validate()
    
    def backup(self) -> Dict[str, Any]:
        """Create configuration backup"""
        return {
            'data': self._data.copy(),
            'metadata': {k: {
                'source': v.source.value,
                'priority': v.priority.value,
                'created_at': v.created_at.isoformat(),
                'updated_at': v.updated_at.isoformat() if v.updated_at else None,
                'version': v.version,
                'encrypted': v.encrypted,
                'cached': v.cached
            } for k, v in self._metadata.items()}
        }
    
    def restore(self, backup: Dict[str, Any]) -> None:
        """Restore configuration from backup"""
        if 'data' in backup:
            self._data = backup['data'].copy()
        
        if 'metadata' in backup:
            self._metadata = {}
            for key, meta in backup['metadata'].items():
                self._metadata[key] = ConfigMetadata(
                    source=ConfigSource(meta['source']),
                    priority=ConfigPriority(meta['priority']),
                    created_at=datetime.fromisoformat(meta['created_at']),
                    updated_at=datetime.fromisoformat(meta['updated_at']) if meta['updated_at'] else None,
                    version=meta['version'],
                    encrypted=meta['encrypted'],
                    cached=meta['cached']
                )
    
    def add_observer(self, observer: IConfigObserver) -> None:
        """Add configuration change observer"""
        self._observers.append(observer)
    
    def remove_observer(self, observer: IConfigObserver) -> None:
        """Remove configuration change observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def set_readonly(self, readonly: bool = True) -> None:
        """Set configuration as readonly"""
        self._readonly = readonly
    
    def is_loaded(self) -> bool:
        """Check if configuration is loaded"""
        return self._loaded
    
    def is_validated(self) -> bool:
        """Check if configuration is validated"""
        return self._validated
    
    def get_metadata(self, key: str) -> Optional[ConfigMetadata]:
        """Get configuration metadata"""
        return self._metadata.get(key)
    
    def get_all_keys(self) -> List[str]:
        """Get all configuration keys"""
        return list(self._data.keys())
    
    def has_key(self, key: str) -> bool:
        """Check if configuration has key"""
        return key in self._data
    
    def remove_key(self, key: str) -> None:
        """Remove configuration key"""
        if self._readonly:
            raise ConfigException("Configuration is readonly")
        
        if key in self._data:
            old_value = self._data[key]
            del self._data[key]
            
            if key in self._metadata:
                del self._metadata[key]
            
            if self._cache:
                self._cache.invalidate(key)
            
            self._notify_observers(key, old_value, None)
    
    # Helper methods
    def _get_nested_value(self, key: str, default: Any = None) -> Any:
        """Get nested configuration value using dot notation"""
        keys = key.split('.')
        value = self._data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def _set_nested_value(self, key: str, value: Any) -> None:
        """Set nested configuration value using dot notation"""
        keys = key.split('.')
        data = self._data
        
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value
    
    def _merge_data(self, new_data: Dict[str, Any]) -> None:
        """Merge new data with existing configuration"""
        def merge_dict(target: Dict, source: Dict) -> None:
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    merge_dict(target[key], value)
                else:
                    target[key] = value
        
        merge_dict(self._data, new_data)
    
    def _is_encrypted(self, key: str) -> bool:
        """Check if key should be encrypted"""
        metadata = self._metadata.get(key)
        return metadata.encrypted if metadata else False
    
    def _should_encrypt(self, key: str) -> bool:
        """Check if key should be encrypted based on naming convention"""
        sensitive_patterns = ['password', 'secret', 'key', 'token', 'credential']
        return any(pattern in key.lower() for pattern in sensitive_patterns)
    
    def _notify_observers(self, key: str, old_value: Any, new_value: Any) -> None:
        """Notify configuration change observers"""
        for observer in self._observers:
            try:
                observer.on_config_changed(key, old_value, new_value)
            except Exception as e:
                self._logger.error(f"Error notifying observer: {e}")
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(name='{self.get_config_name()}', loaded={self._loaded}, validated={self._validated})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"{self.__class__.__name__}(name='{self.get_config_name()}', keys={len(self._data)}, loaded={self._loaded})"
