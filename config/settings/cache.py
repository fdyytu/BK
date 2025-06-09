from .environment import get_env

# Cache Settings
CACHE_TYPE = get_env("CACHE_TYPE", "simple")  # simple, redis, memcached
CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
CACHE_KEY_PREFIX = "myapi_"
CACHE_REDIS_URL = get_env("REDIS_URL", "redis://localhost:6379/0")

# Cache Configuration
CACHE_CONFIG = {
    "DEBUG": False,
    "CACHE_TYPE": CACHE_TYPE,
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT,
    "CACHE_KEY_PREFIX": CACHE_KEY_PREFIX,
    "CACHE_REDIS_URL": CACHE_REDIS_URL
}

# Cache Keys
CACHE_KEYS = {
    "USER_PROFILE": "user_profile_{}",
    "USER_SETTINGS": "user_settings_{}",
    "API_RESPONSE": "api_response_{}"
}