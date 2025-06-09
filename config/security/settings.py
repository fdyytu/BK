from typing import List
from config.base import BaseConfig

class SecurityConfig(BaseConfig):
    """Security configuration implementation"""
    
    def __init__(self):
        self.settings = {}
        self._load_security_modules()
        
    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
        
    def load(self) -> None:
        self.settings = {
            'JWT_SECRET': os.getenv('JWT_SECRET'),
            'JWT_ALGORITHM': os.getenv('JWT_ALGORITHM', 'HS256'),
            'ACCESS_TOKEN_EXPIRE': int(os.getenv('ACCESS_TOKEN_EXPIRE', 3600)),
            'REFRESH_TOKEN_EXPIRE': int(os.getenv('REFRESH_TOKEN_EXPIRE', 86400)),
            'ALLOWED_HOSTS': self._parse_allowed_hosts(),
            'CORS_ORIGINS': self._parse_cors_origins(),
            'SSL_VERIFY': os.getenv('SSL_VERIFY', 'True').lower() == 'true'
        }
        
    def validate(self) -> bool:
        required = ['JWT_SECRET', 'JWT_ALGORITHM']
        return all(key in self.settings for key in required)
        
    def _parse_allowed_hosts(self) -> List[str]:
        """Parse allowed hosts from environment"""
        hosts = os.getenv('ALLOWED_HOSTS', '*')
        return [h.strip() for h in hosts.split(',')]
        
    def _parse_cors_origins(self) -> List[str]:
        """Parse CORS origins from environment"""
        origins = os.getenv('CORS_ORIGINS', '*')
        return [o.strip() for o in origins.split(',')]