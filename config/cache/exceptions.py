class CacheException(Exception):
    """Base exception untuk cache errors"""
    pass

class CacheConnectionError(CacheException):
    """Exception untuk error koneksi cache"""
    pass

class CacheKeyError(CacheException):
    """Exception untuk invalid cache key"""
    pass

class CacheSerializationError(CacheException):
    """Exception untuk error serialisasi/deserialisasi"""
    pass

class CacheTimeoutError(CacheException):
    """Exception untuk timeout error"""
    pass