from datetime import timedelta

# Cache timeouts
DEFAULT_TIMEOUT = timedelta(hours=1)
SHORT_TIMEOUT = timedelta(minutes=5)
MEDIUM_TIMEOUT = timedelta(hours=1)
LONG_TIMEOUT = timedelta(days=1)

# Cache limits
MAX_KEY_LENGTH = 250
MAX_VALUE_SIZE = 1024 * 1024  # 1MB

# Cache status
CACHE_HIT = 'hit'
CACHE_MISS = 'miss'
CACHE_ERROR = 'error'

# Cache prefixes
KEY_PREFIX = 'myapp'
NAMESPACE_SEPARATOR = ':'

# Cache error messages
ERROR_MESSAGES = {
    'connection': 'Failed to connect to cache server',
    'serialization': 'Failed to serialize/deserialize data',
    'key_length': 'Cache key is too long',
    'value_size': 'Cache value is too large',
    'timeout': 'Invalid cache timeout'
}