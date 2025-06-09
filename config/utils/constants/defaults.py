from typing import Any, Dict
from datetime import timedelta

# Default configuration values
DEFAULT_CONFIG: Dict[str, Any] = {
    'environment': 'development',
    'debug': False,
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': None
    },
    'security': {
        'encryption_enabled': True,
        'min_key_length': 2048,
        'token_expiry': 3600,
        'max_attempts': 3
    },
    'caching': {
        'enabled': True,
        'ttl': 300,
        'max_size': 1000
    },
    'timeouts': {
        'connect': 10,
        'read': 30,
        'write': 30
    }
}

# Default validation rules
DEFAULT_VALIDATION_RULES: Dict[str, Any] = {
    'string': {
        'min_length': 1,
        'max_length': 255,
        'allow_empty': False
    },
    'number': {
        'min_value': None,
        'max_value': None,
        'allow_zero': True
    },
    'list': {
        'min_items': 0,
        'max_items': 100,
        'unique_items': True
    }
}

# Default retry settings
DEFAULT_RETRY_SETTINGS: Dict[str, Any] = {
    'max_attempts': 3,
    'initial_delay': 1.0,
    'max_delay': 30.0,
    'backoff_factor': 2.0,
    'jitter': True
}

# Default timeouts
DEFAULT_TIMEOUTS: Dict[str, timedelta] = {
    'connect': timedelta(seconds=10),
    'read': timedelta(seconds=30),
    'write': timedelta(seconds=30),
    'operation': timedelta(minutes=5)
}

# Default security settings
DEFAULT_SECURITY_SETTINGS: Dict[str, Any] = {
    'min_password_length': 8,
    'password_complexity': {
        'uppercase': True,
        'lowercase': True,
        'numbers': True,
        'special': True
    },
    'token_expiry': timedelta(hours=1),
    'max_session_duration': timedelta(days=1),
    'allowed_algorithms': ['HS256', 'RS256', 'ES256']
}

# Default cache settings
DEFAULT_CACHE_SETTINGS: Dict[str, Any] = {
    'ttl': timedelta(minutes=5),
    'max_size': 1000,
    'eviction_policy': 'LRU'
}

# Environment-specific defaults
ENVIRONMENT_DEFAULTS: Dict[str, Dict[str, Any]] = {
    'development': {
        'debug': True,
        'logging': {'level': 'DEBUG'},
        'caching': {'enabled': False}
    },
    'testing': {
        'debug': True,
        'logging': {'level': 'DEBUG'},
        'security': {'encryption_enabled': False}
    },
    'production': {
        'debug': False,
        'logging': {'level': 'WARNING'},
        'security': {'min_key_length': 4096}
    }
}

# Feature flags
DEFAULT_FEATURE_FLAGS: Dict[str, bool] = {
    'advanced_validation': True,
    'async_loading': True,
    'cache_enabled': True,
    'security_checks': True,
    'performance_tracking': False
}