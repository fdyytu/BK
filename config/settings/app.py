from typing import Dict, Any, List
from pydantic import BaseModel, AnyHttpUrl, EmailStr
from .environment import EnvironmentSettings, get_environment

class AppMetadata(BaseModel):
    """Application metadata configuration."""
    name: str
    version: str
    description: str = ""
    authors: List[str] = []
    contact_email: EmailStr
    license: str = "MIT"
    repository_url: str = ""

class ServerConfig(BaseModel):
    """Server configuration settings."""
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = True
    cors_origins: List[AnyHttpUrl] = []
    allowed_hosts: List[str] = ["*"]
    trusted_hosts: List[str] = []

class APIConfig(BaseModel):
    """API configuration settings."""
    prefix: str = "/api"
    version: str = "v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    generate_schemas: bool = True

class PaginationConfig(BaseModel):
    """Pagination configuration settings."""
    default_page: int = 1
    default_size: int = 10
    max_size: int = 100
    page_param: str = "page"
    size_param: str = "size"

class AppSettings(BaseModel):
    """Application settings configuration."""
    
    env: EnvironmentSettings = get_environment()
    metadata: AppMetadata
    server: ServerConfig
    api: APIConfig
    pagination: PaginationConfig
    
    # Response format
    response_format: Dict[str, Any] = {
        "success": True,
        "message": "",
        "data": None,
        "meta": {
            "timestamp": "",
            "code": 200
        }
    }
    
    # Default headers
    default_headers: Dict[str, str] = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block"
    }
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "AppSettings":
        """Create settings from environment."""
        settings = cls(
            env=env,
            metadata=AppMetadata(
                name=os.getenv("APP_NAME", "My API"),
                version=os.getenv("APP_VERSION", "1.0.0"),
                description=os.getenv("APP_DESCRIPTION", ""),
                contact_email=os.getenv("CONTACT_EMAIL", "admin@example.com")
            ),
            server=ServerConfig(
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "8000")),
                workers=int(os.getenv("WORKERS", "4")),
                reload=env.is_development
            ),
            api=APIConfig(
                prefix=os.getenv("API_PREFIX", "/api"),
                version=os.getenv("API_VERSION", "v1"),
                docs_url="/docs" if env.features["api_docs"] else None
            ),
            pagination=PaginationConfig()
        )
        
        if env.is_production:
            settings.server.reload = False
            settings.api.generate_schemas = False
            settings.default_headers.update({
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
            })
        
        return settings