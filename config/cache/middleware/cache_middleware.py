from typing import Callable, Any
from ..client import CacheClient
from ..exceptions import CacheException

class CacheMiddleware:
    """Middleware untuk cache responses"""
    
    def __init__(
        self, 
        app: Any,
        cache_client: CacheClient = None,
        excluded_paths: list = None
    ):
        self.app = app
        self.cache_client = cache_client or CacheClient()
        self.excluded_paths = excluded_paths or []
    
    def __call__(self, environ: dict, start_response: Callable) -> Any:
        # Skip cache for excluded paths
        path = environ.get('PATH_INFO', '')
        if path in self.excluded_paths:
            return self.app(environ, start_response)

        # Try to get from cache
        cache_key = self._build_cache_key(environ)
        cached_response = self.cache_client.get(cache_key)
        
        if cached_response is not None:
            return self._send_cached_response(cached_response, start_response)
            
        # Process request and cache response
        return self._process_and_cache(environ, start_response, cache_key)
    
    def _build_cache_key(self, environ: dict) -> str:
        """Build cache key from request"""
        method = environ.get('REQUEST_METHOD', '')
        path = environ.get('PATH_INFO', '')
        query = environ.get('QUERY_STRING', '')
        return f"response:{method}:{path}:{query}"
    
    def _send_cached_response(self, cached_response: dict, start_response: Callable) -> list:
        """Send cached response"""
        status = cached_response['status']
        headers = cached_response['headers']
        start_response(status, headers)
        return [cached_response['body']]
    
    def _process_and_cache(self, environ: dict, start_response: Callable, cache_key: str) -> Any:
        """Process request and cache response"""
        response = self.app(environ, start_response)
        self.cache_client.set(cache_key, {
            'status': response.status,
            'headers': response.headers,
            'body': response.body
        })
        return response