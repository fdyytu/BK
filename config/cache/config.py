from typing import Dict, Any
from datetime import timedelta

# Default cache configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    'driver': 'redis',
    'serializer': 'json',
    'timeout': timedelta(hours=1),
    'namespace': 'myapp',
    'key_prefix': '',
    
    # Redis specific
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,
        'socket_timeout': 5
    },
    
    # Memcached specific
    'memcached': {
        'servers': ['localhost:11211'],
        'debug': False
    },
    
    # Simple cache specific
    'simple': {
        'threshold': 500,
        'maxsize': 5000
    }
}

# Cache key patterns
KEY_PATTERNS = {
    'user': 'user:{}',
    'session': 'session:{}',
    'rate_limit': 'rate:{}:{}',
    'token': 'token:{}',
}

# Cache regions with different timeouts
CACHE_REGIONS = {
    'short': {
        'timeout': timedelta(minutes=5)
    },
    'medium': {
        'timeout': timedelta(hours=1)
    },
    'long': {
        'timeout': timedelta(days=1)
    }
}