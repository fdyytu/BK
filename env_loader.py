"""
Environment Loader untuk BK API Server
Memuat dan mengelola konfigurasi environment variables
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class EnvironmentLoader:
    """Class untuk memuat dan mengelola environment variables"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Inisialisasi environment loader
        
        Args:
            env_file: Path ke file .env (optional)
        """
        self.env_file = env_file or self._find_env_file()
        self.config = {}
        self.load_environment()
    
    def _find_env_file(self) -> Optional[str]:
        """Mencari file .env di direktori saat ini dan parent directories"""
        current_dir = Path.cwd()
        
        # Cari di direktori saat ini dan parent directories
        for path in [current_dir] + list(current_dir.parents):
            env_path = path / '.env'
            if env_path.exists():
                return str(env_path)
        
        return None
    
    def load_environment(self) -> None:
        """Memuat environment variables dari file .env"""
        try:
            if self.env_file and os.path.exists(self.env_file):
                load_dotenv(self.env_file)
                logger.info(f"✅ Environment file dimuat: {self.env_file}")
            else:
                logger.warning("⚠️  File .env tidak ditemukan, menggunakan environment variables sistem")
            
            # Load semua environment variables
            self._load_config()
            
        except Exception as e:
            logger.error(f"❌ Error memuat environment: {e}")
            raise
    
    def _load_config(self) -> None:
        """Memuat konfigurasi dari environment variables"""
        
        # Application Settings
        self.config.update({
            'APP_NAME': self.get('APP_NAME', 'BK API Server'),
            'APP_VERSION': self.get('APP_VERSION', '1.0.0'),
            'DEBUG': self.get_bool('DEBUG', False),
            'SECRET_KEY': self.get('SECRET_KEY', 'change-this-secret-key'),
        })
        
        # Server Configuration
        self.config.update({
            'HOST': self.get('HOST', '0.0.0.0'),
            'PORT': self.get_int('PORT', 8000),
            'RELOAD': self.get_bool('RELOAD', True),
        })
        
        # Database Configuration
        self.config.update({
            'DATABASE_URL': self.get('DATABASE_URL', 'sqlite:///./bk_database.db'),
        })
        
        # Redis Configuration
        self.config.update({
            'REDIS_URL': self.get('REDIS_URL', 'redis://localhost:6379/0'),
            'REDIS_PASSWORD': self.get('REDIS_PASSWORD', ''),
            'REDIS_DB': self.get_int('REDIS_DB', 0),
        })
        
        # JWT Configuration
        self.config.update({
            'JWT_SECRET_KEY': self.get('JWT_SECRET_KEY', 'jwt-secret-key'),
            'JWT_ALGORITHM': self.get('JWT_ALGORITHM', 'HS256'),
            'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': self.get_int('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 30),
            'JWT_REFRESH_TOKEN_EXPIRE_DAYS': self.get_int('JWT_REFRESH_TOKEN_EXPIRE_DAYS', 7),
        })
        
        # Email Configuration
        self.config.update({
            'SMTP_HOST': self.get('SMTP_HOST', 'smtp.gmail.com'),
            'SMTP_PORT': self.get_int('SMTP_PORT', 587),
            'SMTP_USER': self.get('SMTP_USER', ''),
            'SMTP_PASSWORD': self.get('SMTP_PASSWORD', ''),
            'EMAIL_FROM': self.get('EMAIL_FROM', 'noreply@bk-api.com'),
        })
        
        # External API Keys
        self.config.update({
            'MIDTRANS_SERVER_KEY': self.get('MIDTRANS_SERVER_KEY', ''),
            'MIDTRANS_CLIENT_KEY': self.get('MIDTRANS_CLIENT_KEY', ''),
            'MIDTRANS_IS_PRODUCTION': self.get_bool('MIDTRANS_IS_PRODUCTION', False),
            'XENDIT_SECRET_KEY': self.get('XENDIT_SECRET_KEY', ''),
            'XENDIT_WEBHOOK_TOKEN': self.get('XENDIT_WEBHOOK_TOKEN', ''),
        })
        
        # Notification Services
        self.config.update({
            'FIREBASE_SERVER_KEY': self.get('FIREBASE_SERVER_KEY', ''),
            'ONESIGNAL_APP_ID': self.get('ONESIGNAL_APP_ID', ''),
            'ONESIGNAL_REST_API_KEY': self.get('ONESIGNAL_REST_API_KEY', ''),
        })
        
        # Logging Configuration
        self.config.update({
            'LOG_LEVEL': self.get('LOG_LEVEL', 'INFO'),
            'LOG_FILE': self.get('LOG_FILE', 'logs/bk-api.log'),
            'LOG_MAX_SIZE': self.get_int('LOG_MAX_SIZE', 10485760),
            'LOG_BACKUP_COUNT': self.get_int('LOG_BACKUP_COUNT', 5),
        })
        
        # Security Settings
        self.config.update({
            'CORS_ORIGINS': self.get_list('CORS_ORIGINS', ['http://localhost:3000']),
            'ALLOWED_HOSTS': self.get_list('ALLOWED_HOSTS', ['localhost', '127.0.0.1']),
        })
        
        # Rate Limiting
        self.config.update({
            'RATE_LIMIT_PER_MINUTE': self.get_int('RATE_LIMIT_PER_MINUTE', 60),
            'RATE_LIMIT_BURST': self.get_int('RATE_LIMIT_BURST', 10),
        })
        
        # Cache Settings
        self.config.update({
            'CACHE_TTL': self.get_int('CACHE_TTL', 300),
            'CACHE_MAX_SIZE': self.get_int('CACHE_MAX_SIZE', 1000),
        })
        
        # File Upload Settings
        self.config.update({
            'MAX_FILE_SIZE': self.get_int('MAX_FILE_SIZE', 5242880),
            'ALLOWED_FILE_TYPES': self.get_list('ALLOWED_FILE_TYPES', ['jpg', 'jpeg', 'png', 'pdf']),
            'UPLOAD_DIR': self.get('UPLOAD_DIR', 'uploads/'),
        })
        
        # Monitoring
        self.config.update({
            'ENABLE_METRICS': self.get_bool('ENABLE_METRICS', True),
            'METRICS_PORT': self.get_int('METRICS_PORT', 9090),
        })
    
    def get(self, key: str, default: Any = None) -> str:
        """Mendapatkan environment variable sebagai string"""
        return os.getenv(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Mendapatkan environment variable sebagai integer"""
        try:
            value = os.getenv(key)
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Mendapatkan environment variable sebagai boolean"""
        value = os.getenv(key, '').lower()
        if value in ('true', '1', 'yes', 'on'):
            return True
        elif value in ('false', '0', 'no', 'off'):
            return False
        return default
    
    def get_list(self, key: str, default: List[str] = None) -> List[str]:
        """Mendapatkan environment variable sebagai list"""
        if default is None:
            default = []
        
        value = os.getenv(key)
        if not value:
            return default
        
        # Handle JSON-like format atau comma-separated
        if value.startswith('[') and value.endswith(']'):
            try:
                import json
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        
        # Comma-separated values
        return [item.strip().strip('"').strip("'") for item in value.split(',')]
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Mendapatkan konfigurasi yang sudah dimuat"""
        return self.config.get(key, default)
    
    def get_all_config(self) -> Dict[str, Any]:
        """Mendapatkan semua konfigurasi"""
        return self.config.copy()
    
    def validate_required_config(self, required_keys: List[str]) -> bool:
        """
        Validasi konfigurasi yang wajib ada
        
        Args:
            required_keys: List key yang wajib ada
            
        Returns:
            True jika semua key ada, False jika ada yang missing
        """
        missing_keys = []
        
        for key in required_keys:
            if not self.get_config(key) and not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            logger.error(f"❌ Konfigurasi wajib tidak ditemukan: {', '.join(missing_keys)}")
            return False
        
        return True
    
    def print_config_summary(self) -> None:
        """Menampilkan ringkasan konfigurasi (tanpa sensitive data)"""
        sensitive_keys = [
            'SECRET_KEY', 'JWT_SECRET_KEY', 'SMTP_PASSWORD',
            'MIDTRANS_SERVER_KEY', 'XENDIT_SECRET_KEY', 'FIREBASE_SERVER_KEY'
        ]
        
        print("\n=== Konfigurasi Environment ===")
        for key, value in sorted(self.config.items()):
            if key in sensitive_keys:
                display_value = "***HIDDEN***" if value else "NOT_SET"
            else:
                display_value = value
            print(f"{key}: {display_value}")
        print("=" * 35)

# Instance global
env_loader = EnvironmentLoader()

# Fungsi helper untuk akses mudah
def get_config(key: str, default: Any = None) -> Any:
    """Mendapatkan konfigurasi"""
    return env_loader.get_config(key, default)

def get_env(key: str, default: Any = None) -> str:
    """Mendapatkan environment variable"""
    return env_loader.get(key, default)

def get_env_int(key: str, default: int = 0) -> int:
    """Mendapatkan environment variable sebagai integer"""
    return env_loader.get_int(key, default)

def get_env_bool(key: str, default: bool = False) -> bool:
    """Mendapatkan environment variable sebagai boolean"""
    return env_loader.get_bool(key, default)

def get_env_list(key: str, default: List[str] = None) -> List[str]:
    """Mendapatkan environment variable sebagai list"""
    return env_loader.get_list(key, default)

# Export
__all__ = [
    'EnvironmentLoader',
    'env_loader',
    'get_config',
    'get_env',
    'get_env_int', 
    'get_env_bool',
    'get_env_list'
]
