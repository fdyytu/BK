"""
Configuration Implementations
Provides concrete implementations of configuration interfaces
"""

import os
import json
import yaml
import configparser
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
import hashlib
try:
    from cryptography.fernet import Fernet
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None
import re
from datetime import datetime, timedelta

from .base import (
    IConfigValidator, IConfigLoader, IConfigSerializer, IConfigEncryption, 
    IConfigCache, ConfigSource, ConfigException
)

# Validators
class SchemaValidator(IConfigValidator):
    """Schema-based configuration validator"""
    
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.errors: List[str] = []
        self._logger = logging.getLogger(__name__)
    
    def validate(self, key: str, value: Any) -> bool:
        """Validate configuration value against schema"""
        self.errors.clear()
        
        try:
            if key not in self.schema:
                return True  # Allow unknown keys
            
            expected_type = self.schema[key].get('type')
            required = self.schema[key].get('required', False)
            min_value = self.schema[key].get('min')
            max_value = self.schema[key].get('max')
            pattern = self.schema[key].get('pattern')
            choices = self.schema[key].get('choices')
            
            # Check required
            if required and value is None:
                self.errors.append(f"'{key}' is required")
                return False
            
            if value is None:
                return True
            
            # Check type
            if expected_type and not isinstance(value, expected_type):
                self.errors.append(f"'{key}' must be of type {expected_type.__name__}")
                return False
            
            # Check min/max for numbers
            if isinstance(value, (int, float)):
                if min_value is not None and value < min_value:
                    self.errors.append(f"'{key}' must be >= {min_value}")
                    return False
                if max_value is not None and value > max_value:
                    self.errors.append(f"'{key}' must be <= {max_value}")
                    return False
            
            # Check pattern for strings
            if isinstance(value, str) and pattern:
                if not re.match(pattern, value):
                    self.errors.append(f"'{key}' does not match pattern {pattern}")
                    return False
            
            # Check choices
            if choices and value not in choices:
                self.errors.append(f"'{key}' must be one of {choices}")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Validation error for '{key}': {e}")
            return False
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        return self.errors.copy()

class TypeValidator(IConfigValidator):
    """Type-based configuration validator"""
    
    def __init__(self, type_mapping: Dict[str, type]):
        self.type_mapping = type_mapping
        self.errors: List[str] = []
    
    def validate(self, key: str, value: Any) -> bool:
        """Validate configuration value type"""
        self.errors.clear()
        
        if key in self.type_mapping:
            expected_type = self.type_mapping[key]
            if not isinstance(value, expected_type):
                self.errors.append(f"'{key}' must be of type {expected_type.__name__}")
                return False
        
        return True
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        return self.errors.copy()

# Loaders
class FileLoader(IConfigLoader):
    """File-based configuration loader"""
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    
    def load(self, source: str) -> Dict[str, Any]:
        """Load configuration from file"""
        file_path = Path(source)
        
        if not file_path.exists():
            raise ConfigException(f"Configuration file not found: {source}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    return json.load(f)
                elif file_path.suffix.lower() in ['.yml', '.yaml']:
                    return yaml.safe_load(f) or {}
                elif file_path.suffix.lower() in ['.ini', '.cfg']:
                    config = configparser.ConfigParser()
                    config.read(file_path)
                    return {section: dict(config[section]) for section in config.sections()}
                else:
                    raise ConfigException(f"Unsupported file format: {file_path.suffix}")
        
        except Exception as e:
            self._logger.error(f"Failed to load config from {source}: {e}")
            raise ConfigException(f"Failed to load config from {source}: {e}")
    
    def supports_source(self, source: ConfigSource) -> bool:
        """Check if loader supports source type"""
        return source == ConfigSource.FILE

class EnvironmentLoader(IConfigLoader):
    """Environment variable configuration loader"""
    
    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        self._logger = logging.getLogger(__name__)
    
    def load(self, source: str) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}
        
        for key, value in os.environ.items():
            if self.prefix and not key.startswith(self.prefix):
                continue
            
            # Remove prefix
            config_key = key[len(self.prefix):] if self.prefix else key
            config_key = config_key.lower()
            
            # Try to parse value
            config[config_key] = self._parse_env_value(value)
        
        return config
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value"""
        # Try boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
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
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Return as string
        return value
    
    def supports_source(self, source: ConfigSource) -> bool:
        """Check if loader supports source type"""
        return source == ConfigSource.ENVIRONMENT

# Serializers
class JsonSerializer(IConfigSerializer):
    """JSON configuration serializer"""
    
    def serialize(self, data: Dict[str, Any]) -> str:
        """Serialize configuration data to JSON"""
        try:
            return json.dumps(data, indent=2, default=str)
        except Exception as e:
            raise ConfigException(f"Failed to serialize to JSON: {e}")
    
    def deserialize(self, data: str) -> Dict[str, Any]:
        """Deserialize JSON data to configuration"""
        try:
            return json.loads(data)
        except Exception as e:
            raise ConfigException(f"Failed to deserialize JSON: {e}")

class YamlSerializer(IConfigSerializer):
    """YAML configuration serializer"""
    
    def serialize(self, data: Dict[str, Any]) -> str:
        """Serialize configuration data to YAML"""
        try:
            return yaml.dump(data, default_flow_style=False)
        except Exception as e:
            raise ConfigException(f"Failed to serialize to YAML: {e}")
    
    def deserialize(self, data: str) -> Dict[str, Any]:
        """Deserialize YAML data to configuration"""
        try:
            return yaml.safe_load(data) or {}
        except Exception as e:
            raise ConfigException(f"Failed to deserialize YAML: {e}")

# Encryption
class FernetEncryption(IConfigEncryption):
    """Fernet-based configuration encryption"""
    
    def __init__(self, key: Optional[bytes] = None):
        if not CRYPTOGRAPHY_AVAILABLE:
            raise ConfigException("Cryptography is not available. Install cryptography package to use FernetEncryption.")
        
        if key is None:
            key = Fernet.generate_key()
        self.fernet = Fernet(key)
        self._logger = logging.getLogger(__name__)
    
    def encrypt(self, value: str) -> str:
        """Encrypt configuration value"""
        try:
            encrypted = self.fernet.encrypt(value.encode())
            return encrypted.decode()
        except Exception as e:
            self._logger.error(f"Encryption failed: {e}")
            raise ConfigException(f"Encryption failed: {e}")
    
    def decrypt(self, encrypted_value: str) -> str:
        """Decrypt configuration value"""
        try:
            decrypted = self.fernet.decrypt(encrypted_value.encode())
            return decrypted.decode()
        except Exception as e:
            self._logger.error(f"Decryption failed: {e}")
            raise ConfigException(f"Decryption failed: {e}")

class HashEncryption(IConfigEncryption):
    """Hash-based configuration encryption (one-way)"""
    
    def __init__(self, algorithm: str = 'sha256'):
        self.algorithm = algorithm
        self._logger = logging.getLogger(__name__)
    
    def encrypt(self, value: str) -> str:
        """Hash configuration value"""
        try:
            hash_obj = hashlib.new(self.algorithm)
            hash_obj.update(value.encode())
            return hash_obj.hexdigest()
        except Exception as e:
            self._logger.error(f"Hashing failed: {e}")
            raise ConfigException(f"Hashing failed: {e}")
    
    def decrypt(self, encrypted_value: str) -> str:
        """Cannot decrypt hash - raises exception"""
        raise ConfigException("Hash encryption is one-way, cannot decrypt")

# Cache
class MemoryCache(IConfigCache):
    """In-memory configuration cache"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._ttl: Dict[str, datetime] = {}
        self._logger = logging.getLogger(__name__)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached configuration value"""
        if key in self._cache:
            # Check TTL
            if key in self._ttl and datetime.now() > self._ttl[key]:
                self.invalidate(key)
                return None
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached configuration value"""
        self._cache[key] = value
        if ttl:
            self._ttl[key] = datetime.now() + timedelta(seconds=ttl)
        elif key in self._ttl:
            del self._ttl[key]
    
    def invalidate(self, key: str) -> None:
        """Invalidate cached configuration"""
        if key in self._cache:
            del self._cache[key]
        if key in self._ttl:
            del self._ttl[key]
    
    def clear(self) -> None:
        """Clear all cached configurations"""
        self._cache.clear()
        self._ttl.clear()

class RedisCache(IConfigCache):
    """Redis-based configuration cache"""
    
    def __init__(self, redis_client: Optional['redis.Redis'] = None, prefix: str = "config:"):
        if not REDIS_AVAILABLE:
            raise ConfigException("Redis is not available. Install redis package to use RedisCache.")
        
        self.redis = redis_client or redis.Redis()
        self.prefix = prefix
        self._logger = logging.getLogger(__name__)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached configuration value"""
        try:
            value = self.redis.get(f"{self.prefix}{key}")
            if value:
                return json.loads(value.decode())
            return None
        except Exception as e:
            self._logger.error(f"Redis cache get failed: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached configuration value"""
        try:
            serialized = json.dumps(value, default=str)
            if ttl:
                self.redis.setex(f"{self.prefix}{key}", ttl, serialized)
            else:
                self.redis.set(f"{self.prefix}{key}", serialized)
        except Exception as e:
            self._logger.error(f"Redis cache set failed: {e}")
    
    def invalidate(self, key: str) -> None:
        """Invalidate cached configuration"""
        try:
            self.redis.delete(f"{self.prefix}{key}")
        except Exception as e:
            self._logger.error(f"Redis cache invalidate failed: {e}")
    
    def clear(self) -> None:
        """Clear all cached configurations"""
        try:
            keys = self.redis.keys(f"{self.prefix}*")
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            self._logger.error(f"Redis cache clear failed: {e}")

# Configuration Templates
class DatabaseConfig:
    """Database configuration template"""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            'host': {'type': str, 'required': True},
            'port': {'type': int, 'required': True, 'min': 1, 'max': 65535},
            'database': {'type': str, 'required': True},
            'username': {'type': str, 'required': True},
            'password': {'type': str, 'required': True},
            'pool_size': {'type': int, 'min': 1, 'max': 100},
            'max_overflow': {'type': int, 'min': 0, 'max': 50},
            'pool_timeout': {'type': int, 'min': 1, 'max': 300},
            'ssl_mode': {'type': str, 'choices': ['disable', 'require', 'verify-ca', 'verify-full']}
        }
    
    @staticmethod
    def get_defaults() -> Dict[str, Any]:
        return {
            'host': 'localhost',
            'port': 5432,
            'pool_size': 10,
            'max_overflow': 20,
            'pool_timeout': 30,
            'ssl_mode': 'disable'
        }

class CacheConfig:
    """Cache configuration template"""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            'backend': {'type': str, 'required': True, 'choices': ['memory', 'redis', 'memcached']},
            'host': {'type': str},
            'port': {'type': int, 'min': 1, 'max': 65535},
            'password': {'type': str},
            'db': {'type': int, 'min': 0, 'max': 15},
            'default_ttl': {'type': int, 'min': 1},
            'max_connections': {'type': int, 'min': 1, 'max': 1000}
        }
    
    @staticmethod
    def get_defaults() -> Dict[str, Any]:
        return {
            'backend': 'memory',
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'default_ttl': 3600,
            'max_connections': 10
        }

class SecurityConfig:
    """Security configuration template"""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            'secret_key': {'type': str, 'required': True},
            'jwt_algorithm': {'type': str, 'choices': ['HS256', 'HS384', 'HS512', 'RS256']},
            'jwt_expiration': {'type': int, 'min': 60, 'max': 86400},
            'password_min_length': {'type': int, 'min': 6, 'max': 128},
            'password_require_uppercase': {'type': bool},
            'password_require_lowercase': {'type': bool},
            'password_require_numbers': {'type': bool},
            'password_require_symbols': {'type': bool},
            'max_login_attempts': {'type': int, 'min': 1, 'max': 10},
            'lockout_duration': {'type': int, 'min': 60, 'max': 3600}
        }
    
    @staticmethod
    def get_defaults() -> Dict[str, Any]:
        return {
            'jwt_algorithm': 'HS256',
            'jwt_expiration': 3600,
            'password_min_length': 8,
            'password_require_uppercase': True,
            'password_require_lowercase': True,
            'password_require_numbers': True,
            'password_require_symbols': False,
            'max_login_attempts': 5,
            'lockout_duration': 900
        }

# Factory for creating common configurations
class ConfigFactory:
    """Factory for creating common configuration implementations"""
    
    @staticmethod
    def create_file_loader(file_path: str) -> FileLoader:
        """Create file loader"""
        return FileLoader()
    
    @staticmethod
    def create_env_loader(prefix: str = "") -> EnvironmentLoader:
        """Create environment loader"""
        return EnvironmentLoader(prefix)
    
    @staticmethod
    def create_schema_validator(schema: Dict[str, Any]) -> SchemaValidator:
        """Create schema validator"""
        return SchemaValidator(schema)
    
    @staticmethod
    def create_type_validator(type_mapping: Dict[str, type]) -> TypeValidator:
        """Create type validator"""
        return TypeValidator(type_mapping)
    
    @staticmethod
    def create_memory_cache() -> MemoryCache:
        """Create memory cache"""
        return MemoryCache()
    
    @staticmethod
    def create_redis_cache(redis_client: Optional['redis.Redis'] = None, prefix: str = "config:") -> RedisCache:
        """Create Redis cache"""
        if not REDIS_AVAILABLE:
            raise ConfigException("Redis is not available. Install redis package to use RedisCache.")
        return RedisCache(redis_client, prefix)
    
    @staticmethod
    def create_fernet_encryption(key: Optional[bytes] = None) -> FernetEncryption:
        """Create Fernet encryption"""
        if not CRYPTOGRAPHY_AVAILABLE:
            raise ConfigException("Cryptography is not available. Install cryptography package to use FernetEncryption.")
        return FernetEncryption(key)
    
    @staticmethod
    def create_hash_encryption(algorithm: str = 'sha256') -> HashEncryption:
        """Create hash encryption"""
        return HashEncryption(algorithm)
    
    @staticmethod
    def create_json_serializer() -> JsonSerializer:
        """Create JSON serializer"""
        return JsonSerializer()
    
    @staticmethod
    def create_yaml_serializer() -> YamlSerializer:
        """Create YAML serializer"""
        return YamlSerializer()
