"""
Configuration Module
Provides a comprehensive configuration system with SOLID principles and DRY approach
"""

from .base import (
    BaseConfig,
    IConfigValidator,
    IConfigLoader,
    IConfigSerializer,
    IConfigEncryption,
    IConfigCache,
    IConfigObserver,
    ConfigSource,
    ConfigPriority,
    ConfigMetadata,
    ConfigException,
    ConfigValidationError,
    ConfigLoadError,
    ConfigNotFoundError
)

from .manager import (
    ConfigManager,
    ConfigFactory,
    ConfigBuilder,
    ConfigContainer,
    ConfigStrategy,
    ConfigEnvironment,
    config_manager
)

from .implementations import (
    SchemaValidator,
    TypeValidator,
    FileLoader,
    EnvironmentLoader,
    JsonSerializer,
    YamlSerializer,
    FernetEncryption,
    HashEncryption,
    MemoryCache,
    RedisCache,
    DatabaseConfig,
    CacheConfig,
    SecurityConfig,
    ConfigFactory as ImplConfigFactory
)

from .configs import (
    ApplicationConfig,
    DatabaseConfiguration,
    CacheConfiguration,
    SecurityConfiguration,
    LoggingConfiguration,
    PaymentConfiguration,
    NotificationConfiguration,
    PPOBConfiguration,
    MonitoringConfiguration,
    RateLimitConfiguration,
    TaskConfiguration,
    AppConfigFactory
)

# Version information
__version__ = "2.0.0"
__author__ = "fdygt"
__email__ = "fdygt@example.com"

# Export main classes and functions
__all__ = [
    # Base classes and interfaces
    'BaseConfig',
    'IConfigValidator',
    'IConfigLoader',
    'IConfigSerializer',
    'IConfigEncryption',
    'IConfigCache',
    'IConfigObserver',
    
    # Enums and data classes
    'ConfigSource',
    'ConfigPriority',
    'ConfigMetadata',
    'ConfigStrategy',
    'ConfigEnvironment',
    
    # Exceptions
    'ConfigException',
    'ConfigValidationError',
    'ConfigLoadError',
    'ConfigNotFoundError',
    
    # Manager and patterns
    'ConfigManager',
    'ConfigFactory',
    'ConfigBuilder',
    'ConfigContainer',
    'config_manager',
    
    # Implementations
    'SchemaValidator',
    'TypeValidator',
    'FileLoader',
    'EnvironmentLoader',
    'JsonSerializer',
    'YamlSerializer',
    'FernetEncryption',
    'HashEncryption',
    'MemoryCache',
    'RedisCache',
    
    # Configuration templates
    'DatabaseConfig',
    'CacheConfig',
    'SecurityConfig',
    
    # Application configurations
    'ApplicationConfig',
    'DatabaseConfiguration',
    'CacheConfiguration',
    'SecurityConfiguration',
    'LoggingConfiguration',
    'PaymentConfiguration',
    'NotificationConfiguration',
    'PPOBConfiguration',
    'MonitoringConfiguration',
    'RateLimitConfiguration',
    'TaskConfiguration',
    
    # Factories
    'AppConfigFactory',
    'ImplConfigFactory'
]

# Convenience functions
def get_config(name: str) -> BaseConfig:
    """Get configuration by name from global manager"""
    return config_manager.get_config(name)

def set_config_value(config_name: str, key: str, value: any) -> None:
    """Set configuration value in global manager"""
    config_manager.set_config_value(config_name, key, value)

def get_config_value(config_name: str, key: str, default: any = None) -> any:
    """Get configuration value from global manager"""
    return config_manager.get_config_value(config_name, key, default)

def initialize_configs(config_dir: str = "config", environment: str = "development") -> None:
    """Initialize all application configurations"""
    # Set environment
    env_map = {
        'development': ConfigEnvironment.DEVELOPMENT,
        'testing': ConfigEnvironment.TESTING,
        'staging': ConfigEnvironment.STAGING,
        'production': ConfigEnvironment.PRODUCTION
    }
    config_manager.set_environment(env_map.get(environment, ConfigEnvironment.DEVELOPMENT))
    
    # Create and register all configurations
    configs = AppConfigFactory.create_with_loaders(config_dir)
    
    for name, config in configs.items():
        # Load default values first using the existing load method
        config.load()
        config_manager.register_config(name, config, auto_load=False)
    
    # Load environment-specific configurations
    try:
        config_manager.load_environment_configs(config_dir)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to load environment configs: {e}")
    
    # Validate all configurations after loading defaults and environment configs
    validation_errors = []
    for name, config in config_manager._configs.items():
        if not config.validate():
            validation_errors.extend([f"Config '{name}': {error}" for error in config.get_validation_errors()])
    
    if validation_errors:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Configuration validation warnings: {validation_errors}")
        # Don't raise exception for missing optional configs, just log warnings

def setup_logging_from_config() -> None:
    """Setup logging from configuration"""
    try:
        logging_config = get_config('logging')
        
        import logging.config
        
        # Convert config to logging dict config
        log_config = {
            'version': 1,
            'disable_existing_loggers': logging_config.get('disable_existing_loggers', False),
            'formatters': {
                'default': {
                    'format': logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                    'datefmt': logging_config.get('date_format', '%Y-%m-%d %H:%M:%S')
                },
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
                    'datefmt': logging_config.get('date_format', '%Y-%m-%d %H:%M:%S')
                }
            },
            'handlers': {},
            'loggers': {},
            'root': {
                'level': logging_config.get('level', 'INFO'),
                'handlers': logging_config.get('handlers', ['console'])
            }
        }
        
        # Add console handler
        if 'console' in logging_config.get('handlers', []):
            console_config = logging_config.get('console_handler', {})
            log_config['handlers']['console'] = {
                'class': console_config.get('class', 'logging.StreamHandler'),
                'level': console_config.get('level', 'INFO'),
                'formatter': console_config.get('formatter', 'default')
            }
        
        # Add file handler
        if 'file' in logging_config.get('handlers', []):
            file_config = logging_config.get('file_handler', {})
            log_config['handlers']['file'] = {
                'class': file_config.get('class', 'logging.handlers.RotatingFileHandler'),
                'level': file_config.get('level', 'DEBUG'),
                'formatter': file_config.get('formatter', 'detailed'),
                'filename': file_config.get('filename', 'logs/app.log'),
                'maxBytes': file_config.get('maxBytes', 10485760),
                'backupCount': file_config.get('backupCount', 5)
            }
        
        # Add custom loggers
        for logger_name, logger_config in logging_config.get('loggers', {}).items():
            log_config['loggers'][logger_name] = {
                'level': logger_config.get('level', 'INFO'),
                'handlers': logger_config.get('handlers', []),
                'propagate': logger_config.get('propagate', True)
            }
        
        logging.config.dictConfig(log_config)
        
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Failed to setup logging from config: {e}")

def create_config_builder(config_class: type) -> ConfigBuilder:
    """Create configuration builder"""
    return config_manager.builder(config_class)

def get_health_status() -> dict:
    """Get configuration system health status"""
    return config_manager.get_health_status()

def get_statistics() -> dict:
    """Get configuration statistics"""
    return config_manager.get_statistics()

def backup_configs() -> dict:
    """Backup all configurations"""
    return config_manager.backup_all()

def restore_configs(backup: dict) -> None:
    """Restore configurations from backup"""
    config_manager.restore_all(backup)

def export_configs(filepath: str, format: str = 'json') -> None:
    """Export configurations to file"""
    config_manager.export_to_file(filepath, format)

def import_configs(filepath: str, format: str = 'json') -> None:
    """Import configurations from file"""
    config_manager.import_from_file(filepath, format)

# Configuration decorators
def config_required(config_name: str, key: str):
    """Decorator to ensure configuration value is available"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                value = get_config_value(config_name, key)
                if value is None:
                    raise ConfigException(f"Required configuration '{config_name}.{key}' not found")
                return func(*args, **kwargs)
            except Exception as e:
                raise ConfigException(f"Configuration error: {e}")
        return wrapper
    return decorator

def with_config(config_name: str):
    """Decorator to inject configuration into function"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                config = get_config(config_name)
                kwargs['config'] = config
                return func(*args, **kwargs)
            except Exception as e:
                raise ConfigException(f"Failed to inject config '{config_name}': {e}")
        return wrapper
    return decorator

# Context managers
class ConfigContext:
    """Context manager for temporary configuration changes"""
    
    def __init__(self, config_name: str, **changes):
        self.config_name = config_name
        self.changes = changes
        self.original_values = {}
    
    def __enter__(self):
        config = get_config(self.config_name)
        
        # Store original values
        for key in self.changes:
            if config.has_key(key):
                self.original_values[key] = config.get(key)
        
        # Apply changes
        for key, value in self.changes.items():
            config.set(key, value)
        
        return config
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        config = get_config(self.config_name)
        
        # Restore original values
        for key, value in self.original_values.items():
            config.set(key, value)
        
        # Remove keys that didn't exist originally
        for key in self.changes:
            if key not in self.original_values:
                config.remove_key(key)

def config_context(config_name: str, **changes):
    """Create configuration context manager"""
    return ConfigContext(config_name, **changes)

# Module initialization
import logging
_logger = logging.getLogger(__name__)
_logger.info(f"Configuration module initialized (version {__version__})")
