"""
Enhanced Configuration Manager
Implements advanced design patterns: Factory, Builder, Strategy, Dependency Injection
"""

from typing import Dict, Type, Optional, List, Any, Callable, Union
from abc import ABC, abstractmethod
from enum import Enum
import threading
import logging
from pathlib import Path
import json
import yaml
import os
from datetime import datetime

from .base import (
    BaseConfig, IConfigValidator, IConfigLoader, IConfigSerializer, 
    IConfigEncryption, IConfigCache, IConfigObserver, ConfigSource,
    ConfigException, ConfigLoadError, ConfigValidationError
)

class ConfigStrategy(Enum):
    """Configuration loading strategies"""
    LAZY = "lazy"
    EAGER = "eager"
    ON_DEMAND = "on_demand"

class ConfigEnvironment(Enum):
    """Configuration environments"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class IConfigFactory(ABC):
    """Interface for configuration factories"""
    
    @abstractmethod
    def create_config(self, config_type: str, **kwargs) -> BaseConfig:
        """Create configuration instance"""
        pass
    
    @abstractmethod
    def register_config_type(self, config_type: str, config_class: Type[BaseConfig]) -> None:
        """Register configuration type"""
        pass

class IConfigBuilder(ABC):
    """Interface for configuration builders"""
    
    @abstractmethod
    def with_validator(self, validator: IConfigValidator) -> 'IConfigBuilder':
        """Add validator to configuration"""
        pass
    
    @abstractmethod
    def with_loader(self, loader: IConfigLoader) -> 'IConfigBuilder':
        """Add loader to configuration"""
        pass
    
    @abstractmethod
    def with_cache(self, cache: IConfigCache) -> 'IConfigBuilder':
        """Add cache to configuration"""
        pass
    
    @abstractmethod
    def with_encryption(self, encryption: IConfigEncryption) -> 'IConfigBuilder':
        """Add encryption to configuration"""
        pass
    
    @abstractmethod
    def build(self) -> BaseConfig:
        """Build configuration instance"""
        pass

class ConfigFactory(IConfigFactory):
    """Configuration factory implementation"""
    
    def __init__(self):
        self._config_types: Dict[str, Type[BaseConfig]] = {}
        self._logger = logging.getLogger(__name__)
    
    def create_config(self, config_type: str, **kwargs) -> BaseConfig:
        """Create configuration instance"""
        if config_type not in self._config_types:
            raise ConfigException(f"Unknown config type: {config_type}")
        
        config_class = self._config_types[config_type]
        try:
            return config_class(**kwargs)
        except Exception as e:
            self._logger.error(f"Failed to create config '{config_type}': {e}")
            raise ConfigException(f"Failed to create config '{config_type}': {e}")
    
    def register_config_type(self, config_type: str, config_class: Type[BaseConfig]) -> None:
        """Register configuration type"""
        if not issubclass(config_class, BaseConfig):
            raise ConfigException(f"Config class must inherit from BaseConfig")
        
        self._config_types[config_type] = config_class
        self._logger.debug(f"Registered config type: {config_type}")

class ConfigBuilder(IConfigBuilder):
    """Configuration builder implementation"""
    
    def __init__(self, config_class: Type[BaseConfig]):
        self._config_class = config_class
        self._validator: Optional[IConfigValidator] = None
        self._loader: Optional[IConfigLoader] = None
        self._cache: Optional[IConfigCache] = None
        self._encryption: Optional[IConfigEncryption] = None
        self._serializer: Optional[IConfigSerializer] = None
    
    def with_validator(self, validator: IConfigValidator) -> 'ConfigBuilder':
        """Add validator to configuration"""
        self._validator = validator
        return self
    
    def with_loader(self, loader: IConfigLoader) -> 'ConfigBuilder':
        """Add loader to configuration"""
        self._loader = loader
        return self
    
    def with_cache(self, cache: IConfigCache) -> 'ConfigBuilder':
        """Add cache to configuration"""
        self._cache = cache
        return self
    
    def with_encryption(self, encryption: IConfigEncryption) -> 'ConfigBuilder':
        """Add encryption to configuration"""
        self._encryption = encryption
        return self
    
    def with_serializer(self, serializer: IConfigSerializer) -> 'ConfigBuilder':
        """Add serializer to configuration"""
        self._serializer = serializer
        return self
    
    def build(self) -> BaseConfig:
        """Build configuration instance"""
        return self._config_class(
            validator=self._validator,
            loader=self._loader,
            cache=self._cache,
            encryption=self._encryption,
            serializer=self._serializer
        )

class ConfigContainer:
    """Dependency injection container for configurations"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._lock = threading.Lock()
    
    def register_singleton(self, name: str, instance: Any) -> None:
        """Register singleton service"""
        with self._lock:
            self._singletons[name] = instance
    
    def register_factory(self, name: str, factory: Callable) -> None:
        """Register factory function"""
        with self._lock:
            self._factories[name] = factory
    
    def get(self, name: str) -> Any:
        """Get service instance"""
        with self._lock:
            # Check singletons first
            if name in self._singletons:
                return self._singletons[name]
            
            # Check factories
            if name in self._factories:
                instance = self._factories[name]()
                self._singletons[name] = instance  # Cache as singleton
                return instance
            
            raise ConfigException(f"Service '{name}' not found")
    
    def has(self, name: str) -> bool:
        """Check if service exists"""
        return name in self._singletons or name in self._factories

class ConfigManager:
    """
    Enhanced configuration manager with advanced patterns
    
    Features:
    - Factory pattern for config creation
    - Builder pattern for config construction
    - Strategy pattern for loading strategies
    - Dependency injection container
    - Thread-safe operations
    - Environment-specific configurations
    - Hot reloading capabilities
    - Configuration validation and monitoring
    """
    
    _instance: Optional['ConfigManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ConfigManager':
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._configs: Dict[str, BaseConfig] = {}
        self._factory = ConfigFactory()
        self._container = ConfigContainer()
        self._observers: List[IConfigObserver] = []
        self._strategy = ConfigStrategy.LAZY
        self._environment = ConfigEnvironment.DEVELOPMENT
        self._logger = logging.getLogger(__name__)
        self._config_paths: Dict[str, str] = {}
        self._auto_reload = False
        self._reload_interval = 60  # seconds
        self._last_reload = datetime.now()
        self._lock = threading.RLock()
        self._initialized = True
    
    # Configuration Management
    def register_config(self, name: str, config: BaseConfig, auto_load: bool = True) -> None:
        """Register a configuration"""
        with self._lock:
            if name in self._configs:
                self._logger.warning(f"Config '{name}' already registered, overwriting")
            
            self._configs[name] = config
            
            if auto_load and self._strategy == ConfigStrategy.EAGER:
                try:
                    config.load()
                    config.validate()
                except Exception as e:
                    self._logger.error(f"Failed to load config '{name}': {e}")
                    raise
            
            self._logger.info(f"Registered config: {name}")
    
    def register_config_type(self, config_type: str, config_class: Type[BaseConfig]) -> None:
        """Register configuration type in factory"""
        self._factory.register_config_type(config_type, config_class)
    
    def create_config(self, name: str, config_type: str, **kwargs) -> BaseConfig:
        """Create and register configuration using factory"""
        config = self._factory.create_config(config_type, **kwargs)
        self.register_config(name, config)
        return config
    
    def get_config(self, name: str) -> BaseConfig:
        """Get configuration by name"""
        with self._lock:
            if name not in self._configs:
                raise ConfigException(f"Config '{name}' not found")
            
            config = self._configs[name]
            
            # Lazy loading
            if self._strategy == ConfigStrategy.LAZY and not config.is_loaded():
                try:
                    config.load()
                    config.validate()
                except Exception as e:
                    self._logger.error(f"Failed to lazy load config '{name}': {e}")
                    raise
            
            return config
    
    def get_config_value(self, config_name: str, key: str, default: Any = None) -> Any:
        """Get configuration value directly"""
        try:
            config = self.get_config(config_name)
            return config.get(key, default)
        except Exception as e:
            self._logger.error(f"Failed to get config value '{config_name}.{key}': {e}")
            return default
    
    def set_config_value(self, config_name: str, key: str, value: Any) -> None:
        """Set configuration value directly"""
        config = self.get_config(config_name)
        config.set(key, value)
    
    def has_config(self, name: str) -> bool:
        """Check if configuration exists"""
        return name in self._configs
    
    def remove_config(self, name: str) -> None:
        """Remove configuration"""
        with self._lock:
            if name in self._configs:
                del self._configs[name]
                if name in self._config_paths:
                    del self._config_paths[name]
                self._logger.info(f"Removed config: {name}")
    
    def get_all_configs(self) -> Dict[str, BaseConfig]:
        """Get all configurations"""
        return self._configs.copy()
    
    def get_config_names(self) -> List[str]:
        """Get all configuration names"""
        return list(self._configs.keys())
    
    # Builder Pattern
    def builder(self, config_class: Type[BaseConfig]) -> ConfigBuilder:
        """Get configuration builder"""
        return ConfigBuilder(config_class)
    
    # Environment Management
    def set_environment(self, environment: ConfigEnvironment) -> None:
        """Set current environment"""
        self._environment = environment
        self._logger.info(f"Environment set to: {environment.value}")
    
    def get_environment(self) -> ConfigEnvironment:
        """Get current environment"""
        return self._environment
    
    def load_environment_configs(self, config_dir: str) -> None:
        """Load environment-specific configurations"""
        config_path = Path(config_dir)
        env_file = config_path / f"{self._environment.value}.json"
        
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    env_configs = json.load(f)
                
                for config_name, config_data in env_configs.items():
                    if config_name in self._configs:
                        config = self._configs[config_name]
                        for key, value in config_data.items():
                            config.set(key, value)
                
                self._logger.info(f"Loaded environment configs from: {env_file}")
            except Exception as e:
                self._logger.error(f"Failed to load environment configs: {e}")
                raise ConfigLoadError(f"Failed to load environment configs: {e}")
    
    # Strategy Pattern
    def set_loading_strategy(self, strategy: ConfigStrategy) -> None:
        """Set configuration loading strategy"""
        self._strategy = strategy
        self._logger.info(f"Loading strategy set to: {strategy.value}")
    
    def get_loading_strategy(self) -> ConfigStrategy:
        """Get current loading strategy"""
        return self._strategy
    
    # Bulk Operations
    def load_all(self) -> None:
        """Load all configurations"""
        with self._lock:
            errors = []
            for name, config in self._configs.items():
                try:
                    if not config.is_loaded():
                        config.load()
                except Exception as e:
                    error_msg = f"Failed to load config '{name}': {e}"
                    self._logger.error(error_msg)
                    errors.append(error_msg)
            
            if errors:
                raise ConfigLoadError(f"Failed to load some configurations: {errors}")
            
            self._logger.info("All configurations loaded successfully")
    
    def validate_all(self) -> bool:
        """Validate all configurations"""
        with self._lock:
            errors = []
            for name, config in self._configs.items():
                try:
                    if not config.validate():
                        errors.append(f"Validation failed for config '{name}'")
                except Exception as e:
                    errors.append(f"Validation error for config '{name}': {e}")
            
            if errors:
                self._logger.error(f"Configuration validation errors: {errors}")
                return False
            
            self._logger.info("All configurations validated successfully")
            return True
    
    def reload_all(self) -> None:
        """Reload all configurations"""
        with self._lock:
            for name, config in self._configs.items():
                try:
                    config.reload()
                    self._logger.debug(f"Reloaded config: {name}")
                except Exception as e:
                    self._logger.error(f"Failed to reload config '{name}': {e}")
            
            self._last_reload = datetime.now()
            self._logger.info("All configurations reloaded")
    
    # Hot Reloading
    def enable_auto_reload(self, interval: int = 60) -> None:
        """Enable automatic configuration reloading"""
        self._auto_reload = True
        self._reload_interval = interval
        self._logger.info(f"Auto-reload enabled with interval: {interval}s")
    
    def disable_auto_reload(self) -> None:
        """Disable automatic configuration reloading"""
        self._auto_reload = False
        self._logger.info("Auto-reload disabled")
    
    def check_and_reload(self) -> None:
        """Check if reload is needed and perform it"""
        if not self._auto_reload:
            return
        
        now = datetime.now()
        if (now - self._last_reload).seconds >= self._reload_interval:
            try:
                self.reload_all()
            except Exception as e:
                self._logger.error(f"Auto-reload failed: {e}")
    
    # Observer Pattern
    def add_global_observer(self, observer: IConfigObserver) -> None:
        """Add global configuration observer"""
        self._observers.append(observer)
        
        # Add to all existing configs
        for config in self._configs.values():
            config.add_observer(observer)
    
    def remove_global_observer(self, observer: IConfigObserver) -> None:
        """Remove global configuration observer"""
        if observer in self._observers:
            self._observers.remove(observer)
        
        # Remove from all existing configs
        for config in self._configs.values():
            config.remove_observer(observer)
    
    # Dependency Injection
    def get_container(self) -> ConfigContainer:
        """Get dependency injection container"""
        return self._container
    
    def register_service(self, name: str, service: Any) -> None:
        """Register service in container"""
        self._container.register_singleton(name, service)
    
    def get_service(self, name: str) -> Any:
        """Get service from container"""
        return self._container.get(name)
    
    # Configuration Backup and Restore
    def backup_all(self) -> Dict[str, Any]:
        """Create backup of all configurations"""
        backup = {
            'timestamp': datetime.now().isoformat(),
            'environment': self._environment.value,
            'strategy': self._strategy.value,
            'configs': {}
        }
        
        for name, config in self._configs.items():
            try:
                backup['configs'][name] = config.backup()
            except Exception as e:
                self._logger.error(f"Failed to backup config '{name}': {e}")
        
        return backup
    
    def restore_all(self, backup: Dict[str, Any]) -> None:
        """Restore all configurations from backup"""
        if 'configs' not in backup:
            raise ConfigException("Invalid backup format")
        
        for name, config_backup in backup['configs'].items():
            if name in self._configs:
                try:
                    self._configs[name].restore(config_backup)
                except Exception as e:
                    self._logger.error(f"Failed to restore config '{name}': {e}")
    
    # Health and Monitoring
    def get_health_status(self) -> Dict[str, Any]:
        """Get configuration system health status"""
        status = {
            'total_configs': len(self._configs),
            'loaded_configs': sum(1 for c in self._configs.values() if c.is_loaded()),
            'validated_configs': sum(1 for c in self._configs.values() if c.is_validated()),
            'environment': self._environment.value,
            'strategy': self._strategy.value,
            'auto_reload': self._auto_reload,
            'last_reload': self._last_reload.isoformat(),
            'configs': {}
        }
        
        for name, config in self._configs.items():
            status['configs'][name] = {
                'loaded': config.is_loaded(),
                'validated': config.is_validated(),
                'keys_count': len(config.get_all_keys()) if config.is_loaded() else 0
            }
        
        return status
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get configuration statistics"""
        total_keys = 0
        config_sizes = {}
        
        for name, config in self._configs.items():
            if config.is_loaded():
                keys = config.get_all_keys()
                config_sizes[name] = len(keys)
                total_keys += len(keys)
        
        return {
            'total_configurations': len(self._configs),
            'total_keys': total_keys,
            'average_keys_per_config': total_keys / len(self._configs) if self._configs else 0,
            'config_sizes': config_sizes,
            'memory_usage': self._estimate_memory_usage()
        }
    
    def _estimate_memory_usage(self) -> str:
        """Estimate memory usage of configurations"""
        # Simple estimation based on string representation
        total_size = 0
        for config in self._configs.values():
            if config.is_loaded():
                total_size += len(str(config))
        
        if total_size < 1024:
            return f"{total_size} bytes"
        elif total_size < 1024 * 1024:
            return f"{total_size / 1024:.2f} KB"
        else:
            return f"{total_size / (1024 * 1024):.2f} MB"
    
    # Utility Methods
    def clear_all(self) -> None:
        """Clear all configurations"""
        with self._lock:
            self._configs.clear()
            self._config_paths.clear()
            self._logger.info("All configurations cleared")
    
    def export_to_file(self, filepath: str, format: str = 'json') -> None:
        """Export all configurations to file"""
        backup = self.backup_all()
        
        try:
            with open(filepath, 'w') as f:
                if format.lower() == 'json':
                    json.dump(backup, f, indent=2, default=str)
                elif format.lower() == 'yaml':
                    yaml.dump(backup, f, default_flow_style=False)
                else:
                    raise ConfigException(f"Unsupported format: {format}")
            
            self._logger.info(f"Configurations exported to: {filepath}")
        except Exception as e:
            self._logger.error(f"Failed to export configurations: {e}")
            raise
    
    def import_from_file(self, filepath: str, format: str = 'json') -> None:
        """Import configurations from file"""
        try:
            with open(filepath, 'r') as f:
                if format.lower() == 'json':
                    backup = json.load(f)
                elif format.lower() == 'yaml':
                    backup = yaml.safe_load(f)
                else:
                    raise ConfigException(f"Unsupported format: {format}")
            
            self.restore_all(backup)
            self._logger.info(f"Configurations imported from: {filepath}")
        except Exception as e:
            self._logger.error(f"Failed to import configurations: {e}")
            raise
    
    def __str__(self) -> str:
        """String representation"""
        return f"ConfigManager(configs={len(self._configs)}, env={self._environment.value}, strategy={self._strategy.value})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"ConfigManager(configs={list(self._configs.keys())}, environment={self._environment.value})"

# Global instance
config_manager = ConfigManager()
