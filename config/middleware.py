from typing import List, Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from .settings import get_settings

settings = get_settings()

def setup_middlewares(app: FastAPI) -> None:
    """Setup application middlewares."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    # Trusted host middleware
    if settings.server.trusted_hosts:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.server.trusted_hosts
        )
    
    # Compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Custom security middleware
    @app.middleware("http")
    async def security_headers(request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        for header, value in settings.default_headers.items():
            response.headers[header] = value
            
        return response
    
    # Request ID middleware
    @app.middleware("http")
    async def add_request_id(request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response