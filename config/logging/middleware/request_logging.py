from typing import Callable
from fastapi import Request, Response
import time
import logging
from uuid import uuid4

class RequestLoggingMiddleware:
    def __init__(self):
        self.logger = logging.getLogger('request')

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid4())
        start_time = time.time()
        
        # Pre-request logging
        self.logger.info(
            'Request started',
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'client_ip': request.client.host,
                'user_agent': request.headers.get('user-agent'),
                'timestamp_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            }
        )

        response = await call_next(request)
        
        # Post-request logging
        process_time = time.time() - start_time
        self.logger.info(
            'Request completed',
            extra={
                'request_id': request_id,
                'status_code': response.status_code,
                'process_time_ms': round(process_time * 1000, 2),
                'timestamp_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            }
        )
        
        return response