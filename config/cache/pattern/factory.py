from typing import Dict, Type, Any
from ..drivers import RedisDriver, MemcachedDriver, SimpleDriver
from ..serializers import JsonSerializer, PickleSerializer
from ..exceptions import CacheException

class CacheFactory:
    """Factory untuk membuat cache instances"""
    
    _drivers: Dict[str, Type] = {
        'redis': RedisDriver,
        'memcached': MemcachedDriver,
        'simple': SimpleDriver
    }
    
    _serializers: Dict[str, Type] = {
        'json': JsonSerializer,
        'pickle': PickleSerializer
    }
    
    @classmethod
    def create_driver(cls, driver_type: str, **config: Any) -> Any:
        """Create cache driver instance"""
        if driver_type not in cls._drivers:
            raise CacheException(f"Unknown driver type: {driver_type}")
        return cls._drivers[driver_type](**config)
    
    @classmethod
    def create_serializer(cls, serializer_type: str) -> Any:
        """Create serializer instance"""
        if serializer_type not in cls._serializers:
            raise CacheException(f"Unknown serializer type: {serializer_type}")
        return cls._serializers[serializer_type]()