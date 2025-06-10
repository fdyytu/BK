# Enhanced Configuration System

A comprehensive, enterprise-grade configuration management system implementing SOLID principles and advanced design patterns for the Digital Product & PPOB Platform API.

## Features

### Core Features
- **SOLID Principles Implementation**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Advanced Design Patterns**: Factory, Builder, Strategy, Observer, Singleton, Dependency Injection
- **Environment-Specific Configurations**: Development, Testing, Staging, Production
- **Multiple Configuration Sources**: Files (JSON, YAML, INI), Environment Variables, Database, Remote APIs
- **Configuration Validation**: Schema-based validation with type checking, constraints, and custom rules
- **Caching System**: Memory and Redis-based caching with TTL support
- **Encryption Support**: Fernet and hash-based encryption for sensitive configuration values
- **Hot Reloading**: Automatic configuration reloading with configurable intervals
- **Monitoring & Health Checks**: Real-time configuration system monitoring and health status
- **Backup & Restore**: Complete configuration backup and restore functionality
- **Thread-Safe Operations**: Full thread safety for concurrent access

### Advanced Features
- **Configuration Observers**: Real-time change notifications
- **Context Managers**: Temporary configuration changes
- **Decorators**: Configuration injection and validation decorators
- **Nested Configuration Access**: Dot notation support for nested values
- **Configuration Versioning**: Version tracking and migration support
- **Performance Optimization**: Efficient caching and lazy loading
- **Error Handling**: Comprehensive error handling with detailed logging

## Architecture

### Class Hierarchy
```
BaseConfig (Abstract)
├── ApplicationConfig
├── DatabaseConfiguration
├── CacheConfiguration
├── SecurityConfiguration
├── LoggingConfiguration
├── PaymentConfiguration
├── NotificationConfiguration
├── PPOBConfiguration
├── MonitoringConfiguration
├── RateLimitConfiguration
└── TaskConfiguration
```

### Interface Implementations
```
IConfigValidator
├── SchemaValidator
└── TypeValidator

IConfigLoader
├── FileLoader
└── EnvironmentLoader

IConfigCache
├── MemoryCache
└── RedisCache

IConfigEncryption
├── FernetEncryption
└── HashEncryption

IConfigSerializer
├── JsonSerializer
└── YamlSerializer
```

## Quick Start

### Basic Usage

```python
from config import initialize_configs, get_config_value, set_config_value

# Initialize configuration system
initialize_configs(environment="development")

# Get configuration values
app_name = get_config_value('application', 'app_name')
debug_mode = get_config_value('application', 'debug', False)
db_host = get_config_value('database', 'host', 'localhost')

# Set configuration values
set_config_value('application', 'custom_setting', 'custom_value')
```

### Advanced Usage with Builder Pattern

```python
from config import (
    create_config_builder, ApplicationConfig, 
    SchemaValidator, FileLoader, MemoryCache
)

# Create custom configuration
validator = SchemaValidator({
    'api_key': {'type': str, 'required': True},
    'timeout': {'type': int, 'min': 1, 'max': 300}
})

config = (create_config_builder(ApplicationConfig)
          .with_validator(validator)
          .with_loader(FileLoader())
          .with_cache(MemoryCache())
          .build())

config.set('api_key', 'your-api-key')
config.set('timeout', 30)
```

### Using Context Managers

```python
from config import config_context, get_config_value

# Temporary configuration changes
with config_context('application', debug=True, test_mode=True):
    debug = get_config_value('application', 'debug')  # True
    test_mode = get_config_value('application', 'test_mode')  # True

# Values are automatically restored after context
```

### Configuration Decorators

```python
from config import config_required, with_config

@config_required('application', 'app_name')
def function_requiring_config():
    # Function will only execute if app_name is configured
    pass

@with_config('database')
def function_with_config(config=None):
    # Database config is automatically injected
    host = config.get('host')
    port = config.get('port')
```

## Configuration Files

### Environment-Specific Configuration

The system supports environment-specific configuration files:

- `config/settings/development.json`
- `config/settings/testing.json`
- `config/settings/staging.json`
- `config/settings/production.json`

### Configuration Structure

```json
{
    "application": {
        "app_name": "Digital Product & PPOB Platform API",
        "debug": false,
        "host": "0.0.0.0",
        "port": 8000
    },
    "database": {
        "host": "localhost",
        "port": 5432,
        "database": "digital_platform",
        "username": "user",
        "password": "password"
    },
    "cache": {
        "backend": "redis",
        "host": "localhost",
        "port": 6379
    }
}
```

## Configuration Types

### Application Configuration
- Basic application settings (name, version, debug mode)
- Server configuration (host, port, workers)
- API settings (prefix, documentation URLs)
- CORS configuration
- Pagination settings

### Database Configuration
- Connection settings (host, port, database, credentials)
- Connection pooling (pool size, overflow, timeout)
- SSL configuration
- Query optimization settings

### Cache Configuration
- Backend selection (memory, Redis, Memcached)
- Connection settings
- TTL configuration
- Performance tuning

### Security Configuration
- Secret keys and tokens
- JWT configuration
- Password policies
- Authentication settings
- Rate limiting rules

### Payment Configuration
- Multiple payment gateway support (Midtrans, Xendit, DOKU)
- Sandbox/production modes
- API credentials
- Webhook configurations
- Transaction limits

### PPOB Configuration
- Provider settings (MobilePulsa, etc.)
- Product categories (pulsa, data, PLN, games)
- Commission rates
- Transaction processing settings

### Monitoring Configuration
- Metrics collection
- Health check endpoints
- Alerting rules
- Tracing configuration
- Performance monitoring

## Environment Variables

The system supports environment variable overrides with prefixes:

```bash
# Application settings
APPLICATION_DEBUG=true
APPLICATION_HOST=127.0.0.1
APPLICATION_PORT=8000

# Database settings
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=secret

# Security settings
SECURITY_SECRET_KEY=your-secret-key
SECURITY_JWT_EXPIRATION=3600
```

## Validation

### Schema Validation

```python
schema = {
    'host': {'type': str, 'required': True},
    'port': {'type': int, 'min': 1, 'max': 65535},
    'timeout': {'type': int, 'min': 1, 'max': 300},
    'ssl_mode': {'type': str, 'choices': ['disable', 'require', 'verify-full']}
}

validator = SchemaValidator(schema)
config = ApplicationConfig(validator=validator)
```

### Type Validation

```python
type_mapping = {
    'debug': bool,
    'port': int,
    'timeout': float,
    'app_name': str
}

validator = TypeValidator(type_mapping)
```

## Caching

### Memory Cache

```python
from config import MemoryCache

cache = MemoryCache()
config = ApplicationConfig(cache=cache)
```

### Redis Cache

```python
from config import RedisCache
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = RedisCache(redis_client, prefix="config:")
config = ApplicationConfig(cache=cache)
```

## Encryption

### Fernet Encryption

```python
from config import FernetEncryption

encryption = FernetEncryption()
config = SecurityConfiguration(encryption=encryption)

# Sensitive values are automatically encrypted
config.set('secret_key', 'my-secret-key')
```

### Hash Encryption

```python
from config import HashEncryption

encryption = HashEncryption('sha256')
config = SecurityConfiguration(encryption=encryption)

# Values are hashed (one-way)
config.set('password_hash', 'user-password')
```

## Monitoring

### Health Status

```python
from config import get_health_status

health = get_health_status()
print(f"Total configs: {health['total_configs']}")
print(f"Loaded configs: {health['loaded_configs']}")
print(f"Environment: {health['environment']}")
```

### Statistics

```python
from config import get_statistics

stats = get_statistics()
print(f"Total configurations: {stats['total_configurations']}")
print(f"Total keys: {stats['total_keys']}")
print(f"Memory usage: {stats['memory_usage']}")
```

## Backup & Restore

### Creating Backups

```python
from config import backup_configs, export_configs

# Create in-memory backup
backup = backup_configs()

# Export to file
export_configs('config_backup.json', format='json')
export_configs('config_backup.yaml', format='yaml')
```

### Restoring Configurations

```python
from config import restore_configs, import_configs

# Restore from in-memory backup
restore_configs(backup)

# Import from file
import_configs('config_backup.json', format='json')
```

## Error Handling

The system provides comprehensive error handling:

```python
from config import (
    ConfigException, ConfigValidationError, 
    ConfigLoadError, ConfigNotFoundError
)

try:
    config = get_config('non_existent')
except ConfigNotFoundError as e:
    print(f"Configuration not found: {e}")

try:
    config.set('invalid_key', 'invalid_value')
except ConfigValidationError as e:
    print(f"Validation failed: {e}")
```

## Performance Considerations

### Lazy Loading
- Configurations are loaded on-demand by default
- Use `ConfigStrategy.EAGER` for immediate loading
- Use `ConfigStrategy.LAZY` for memory efficiency

### Caching
- Enable caching for frequently accessed values
- Use Redis cache for distributed applications
- Configure appropriate TTL values

### Thread Safety
- All operations are thread-safe
- Use connection pooling for database configurations
- Implement proper locking for custom implementations

## Best Practices

### Configuration Organization
1. Group related settings in dedicated configuration classes
2. Use environment-specific files for different deployment stages
3. Keep sensitive data in environment variables
4. Use validation to ensure configuration integrity

### Security
1. Encrypt sensitive configuration values
2. Use strong secret keys and rotate them regularly
3. Limit access to configuration files
4. Audit configuration changes

### Performance
1. Enable caching for frequently accessed configurations
2. Use lazy loading for large configuration sets
3. Implement proper connection pooling
4. Monitor configuration system performance

### Maintenance
1. Regular backup of configurations
2. Version control for configuration files
3. Document configuration changes
4. Test configuration changes in staging environment

## API Reference

### Core Functions

- `initialize_configs(config_dir, environment)`: Initialize configuration system
- `get_config(name)`: Get configuration instance
- `get_config_value(config_name, key, default)`: Get configuration value
- `set_config_value(config_name, key, value)`: Set configuration value
- `create_config_builder(config_class)`: Create configuration builder

### Monitoring Functions

- `get_health_status()`: Get system health status
- `get_statistics()`: Get system statistics
- `backup_configs()`: Create configuration backup
- `restore_configs(backup)`: Restore from backup

### Utility Functions

- `export_configs(filepath, format)`: Export to file
- `import_configs(filepath, format)`: Import from file
- `config_context(config_name, **changes)`: Create context manager
- `setup_logging_from_config()`: Setup logging from configuration

## Examples

See `config/examples.py` for comprehensive usage examples including:
- Basic configuration usage
- Advanced builder pattern usage
- Context manager examples
- Decorator usage
- Monitoring and health checks
- Backup and restore operations
- Error handling
- Performance testing

## Contributing

1. Follow SOLID principles when adding new features
2. Implement proper interfaces for extensibility
3. Add comprehensive tests for new functionality
4. Update documentation for API changes
5. Follow existing code style and patterns

## License

This configuration system is part of the Digital Product & PPOB Platform API project.
