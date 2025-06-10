"""
Concrete Configuration Classes
Application-specific configuration implementations
"""

from typing import Dict, Any, List, Optional
import os
from pathlib import Path
import logging

from .base import BaseConfig, ConfigMetadata, ConfigSource, ConfigPriority
from .implementations import (
    SchemaValidator, FileLoader, EnvironmentLoader, MemoryCache,
    DatabaseConfig, CacheConfig, SecurityConfig
)

class ApplicationConfig(BaseConfig):
    """Main application configuration"""
    
    def get_config_name(self) -> str:
        return "application"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'app_name': 'Digital Product & PPOB Platform API',
            'app_version': '1.0.0',
            'debug': False,
            'environment': 'production',
            'host': '0.0.0.0',
            'port': 8000,
            'workers': 4,
            'max_request_size': 16 * 1024 * 1024,  # 16MB
            'request_timeout': 30,
            'cors_enabled': True,
            'cors_origins': ['*'],
            'cors_methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'cors_headers': ['*'],
            'api_prefix': '/api/v1',
            'docs_url': '/docs',
            'redoc_url': '/redoc',
            'openapi_url': '/openapi.json',
            'timezone': 'UTC',
            'locale': 'en_US',
            'pagination_default_limit': 20,
            'pagination_max_limit': 100
        }
    
    def get_required_keys(self) -> List[str]:
        return ['app_name', 'host', 'port']

class DatabaseConfiguration(BaseConfig):
    """Database configuration"""
    
    def get_config_name(self) -> str:
        return "database"
    
    def get_default_values(self) -> Dict[str, Any]:
        return DatabaseConfig.get_defaults()
    
    def get_required_keys(self) -> List[str]:
        return ['host', 'port', 'database', 'username', 'password']

class CacheConfiguration(BaseConfig):
    """Cache configuration"""
    
    def get_config_name(self) -> str:
        return "cache"
    
    def get_default_values(self) -> Dict[str, Any]:
        return CacheConfig.get_defaults()
    
    def get_required_keys(self) -> List[str]:
        return ['backend']

class SecurityConfiguration(BaseConfig):
    """Security configuration"""
    
    def get_config_name(self) -> str:
        return "security"
    
    def get_default_values(self) -> Dict[str, Any]:
        defaults = SecurityConfig.get_defaults()
        # Generate secret key if not provided
        if 'secret_key' not in defaults:
            import secrets
            defaults['secret_key'] = secrets.token_urlsafe(32)
        return defaults
    
    def get_required_keys(self) -> List[str]:
        return ['secret_key']

class LoggingConfiguration(BaseConfig):
    """Logging configuration"""
    
    def get_config_name(self) -> str:
        return "logging"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'date_format': '%Y-%m-%d %H:%M:%S',
            'handlers': ['console', 'file'],
            'console_handler': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default'
            },
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': 'logs/app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'loggers': {
                'uvicorn': {'level': 'INFO'},
                'sqlalchemy': {'level': 'WARNING'},
                'redis': {'level': 'WARNING'}
            },
            'disable_existing_loggers': False
        }
    
    def get_required_keys(self) -> List[str]:
        return ['level', 'format']

class PaymentConfiguration(BaseConfig):
    """Payment gateway configuration"""
    
    def get_config_name(self) -> str:
        return "payment"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'default_gateway': 'midtrans',
            'gateways': {
                'midtrans': {
                    'enabled': True,
                    'sandbox': True,
                    'server_key': '',
                    'client_key': '',
                    'merchant_id': '',
                    'timeout': 30,
                    'notification_url': '/api/v1/payment/midtrans/notification',
                    'return_url': '/payment/success',
                    'error_url': '/payment/error'
                },
                'xendit': {
                    'enabled': False,
                    'sandbox': True,
                    'secret_key': '',
                    'public_key': '',
                    'webhook_token': '',
                    'timeout': 30,
                    'callback_url': '/api/v1/payment/xendit/callback'
                },
                'doku': {
                    'enabled': False,
                    'sandbox': True,
                    'mall_id': '',
                    'shared_key': '',
                    'timeout': 30,
                    'notify_url': '/api/v1/payment/doku/notify'
                }
            },
            'auto_settlement': True,
            'settlement_delay': 24,  # hours
            'max_retry_attempts': 3,
            'retry_delay': 300,  # seconds
            'supported_currencies': ['IDR'],
            'min_amount': 1000,
            'max_amount': 50000000
        }
    
    def get_required_keys(self) -> List[str]:
        return ['default_gateway', 'gateways']

class NotificationConfiguration(BaseConfig):
    """Notification system configuration"""
    
    def get_config_name(self) -> str:
        return "notification"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'email': {
                'enabled': True,
                'provider': 'smtp',
                'smtp': {
                    'host': 'localhost',
                    'port': 587,
                    'username': '',
                    'password': '',
                    'use_tls': True,
                    'use_ssl': False,
                    'timeout': 30
                },
                'from_email': 'noreply@example.com',
                'from_name': 'Digital Platform',
                'templates_dir': 'templates/email',
                'max_retry_attempts': 3
            },
            'sms': {
                'enabled': True,
                'provider': 'twilio',
                'twilio': {
                    'account_sid': '',
                    'auth_token': '',
                    'from_number': ''
                },
                'max_retry_attempts': 3
            },
            'push': {
                'enabled': True,
                'provider': 'firebase',
                'firebase': {
                    'server_key': '',
                    'project_id': ''
                },
                'max_retry_attempts': 3
            },
            'webhook': {
                'enabled': True,
                'timeout': 30,
                'max_retry_attempts': 3,
                'retry_delay': 60
            }
        }
    
    def get_required_keys(self) -> List[str]:
        return []

class PPOBConfiguration(BaseConfig):
    """PPOB (Payment Point Online Bank) configuration"""
    
    def get_config_name(self) -> str:
        return "ppob"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'providers': {
                'mobilepulsa': {
                    'enabled': True,
                    'api_key': '',
                    'secret_key': '',
                    'base_url': 'https://api.mobilepulsa.net/v1',
                    'timeout': 30,
                    'max_retry_attempts': 3
                }
            },
            'categories': {
                'pulsa': {
                    'enabled': True,
                    'commission_rate': 0.05,
                    'min_amount': 5000,
                    'max_amount': 1000000
                },
                'data': {
                    'enabled': True,
                    'commission_rate': 0.03,
                    'min_amount': 5000,
                    'max_amount': 500000
                },
                'pln': {
                    'enabled': True,
                    'commission_rate': 0.02,
                    'min_amount': 20000,
                    'max_amount': 5000000
                },
                'game': {
                    'enabled': True,
                    'commission_rate': 0.08,
                    'min_amount': 5000,
                    'max_amount': 2000000
                }
            },
            'auto_process': True,
            'process_delay': 5,  # seconds
            'inquiry_timeout': 30,
            'transaction_timeout': 60,
            'status_check_interval': 30,
            'max_status_checks': 10
        }
    
    def get_required_keys(self) -> List[str]:
        return ['providers']

class MonitoringConfiguration(BaseConfig):
    """Monitoring and metrics configuration"""
    
    def get_config_name(self) -> str:
        return "monitoring"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'enabled': True,
            'metrics': {
                'enabled': True,
                'endpoint': '/metrics',
                'include_in_schema': False,
                'collect_default_metrics': True,
                'custom_metrics': {
                    'request_duration': True,
                    'request_count': True,
                    'error_count': True,
                    'active_connections': True
                }
            },
            'health_check': {
                'enabled': True,
                'endpoint': '/health',
                'include_in_schema': False,
                'checks': {
                    'database': True,
                    'cache': True,
                    'external_apis': True,
                    'disk_space': True,
                    'memory_usage': True
                }
            },
            'alerting': {
                'enabled': True,
                'channels': {
                    'email': {
                        'enabled': True,
                        'recipients': ['admin@example.com']
                    },
                    'slack': {
                        'enabled': False,
                        'webhook_url': '',
                        'channel': '#alerts'
                    }
                },
                'rules': {
                    'high_error_rate': {
                        'threshold': 0.05,
                        'window': 300,  # seconds
                        'severity': 'critical'
                    },
                    'high_response_time': {
                        'threshold': 2.0,  # seconds
                        'window': 300,
                        'severity': 'warning'
                    },
                    'low_disk_space': {
                        'threshold': 0.1,  # 10%
                        'severity': 'warning'
                    }
                }
            },
            'tracing': {
                'enabled': False,
                'service_name': 'digital-platform-api',
                'jaeger': {
                    'agent_host': 'localhost',
                    'agent_port': 6831
                }
            }
        }
    
    def get_required_keys(self) -> List[str]:
        return []

class RateLimitConfiguration(BaseConfig):
    """Rate limiting configuration"""
    
    def get_config_name(self) -> str:
        return "rate_limit"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'enabled': True,
            'storage': 'redis',
            'default_limits': {
                'requests_per_minute': 60,
                'requests_per_hour': 1000,
                'requests_per_day': 10000
            },
            'endpoint_limits': {
                '/api/v1/auth/login': {
                    'requests_per_minute': 5,
                    'requests_per_hour': 20
                },
                '/api/v1/auth/register': {
                    'requests_per_minute': 3,
                    'requests_per_hour': 10
                },
                '/api/v1/payment/*': {
                    'requests_per_minute': 30,
                    'requests_per_hour': 500
                }
            },
            'user_type_limits': {
                'guest': {
                    'requests_per_minute': 30,
                    'requests_per_hour': 500
                },
                'user': {
                    'requests_per_minute': 60,
                    'requests_per_hour': 1000
                },
                'partner': {
                    'requests_per_minute': 120,
                    'requests_per_hour': 2000
                },
                'admin': {
                    'requests_per_minute': 300,
                    'requests_per_hour': 5000
                }
            },
            'whitelist_ips': [],
            'blacklist_ips': [],
            'headers': {
                'limit': 'X-RateLimit-Limit',
                'remaining': 'X-RateLimit-Remaining',
                'reset': 'X-RateLimit-Reset'
            },
            'error_message': 'Rate limit exceeded. Please try again later.',
            'error_status_code': 429
        }
    
    def get_required_keys(self) -> List[str]:
        return []

class TaskConfiguration(BaseConfig):
    """Background task configuration"""
    
    def get_config_name(self) -> str:
        return "tasks"
    
    def get_default_values(self) -> Dict[str, Any]:
        return {
            'broker': 'redis',
            'backend': 'redis',
            'redis': {
                'host': 'localhost',
                'port': 6379,
                'db': 1,
                'password': None
            },
            'rabbitmq': {
                'host': 'localhost',
                'port': 5672,
                'username': 'guest',
                'password': 'guest',
                'virtual_host': '/'
            },
            'worker': {
                'concurrency': 4,
                'max_tasks_per_child': 1000,
                'task_time_limit': 300,
                'task_soft_time_limit': 240
            },
            'beat': {
                'enabled': True,
                'schedule': {
                    'cleanup_expired_sessions': {
                        'task': 'tasks.maintenance.cleanup.session_cleanup',
                        'schedule': 3600.0  # every hour
                    },
                    'update_exchange_rates': {
                        'task': 'tasks.ppob.maintenance.price_update',
                        'schedule': 1800.0  # every 30 minutes
                    },
                    'generate_daily_reports': {
                        'task': 'tasks.reporting.financial.daily_report',
                        'schedule': {
                            'hour': 1,
                            'minute': 0
                        }
                    }
                }
            },
            'routes': {
                'email': 'email_queue',
                'sms': 'sms_queue',
                'push': 'push_queue',
                'payment': 'payment_queue',
                'ppob': 'ppob_queue',
                'reports': 'reports_queue'
            },
            'retry': {
                'max_retries': 3,
                'retry_delay': 60,
                'retry_backoff': True,
                'retry_jitter': True
            }
        }
    
    def get_required_keys(self) -> List[str]:
        return ['broker']

# Configuration factory for creating application configs
class AppConfigFactory:
    """Factory for creating application-specific configurations"""
    
    @staticmethod
    def create_all_configs() -> Dict[str, BaseConfig]:
        """Create all application configurations"""
        configs = {}
        
        # Create validators for each config type
        app_validator = SchemaValidator({
            'app_name': {'type': str, 'required': True},
            'port': {'type': int, 'min': 1, 'max': 65535},
            'workers': {'type': int, 'min': 1, 'max': 32},
            'debug': {'type': bool}
        })
        
        db_validator = SchemaValidator(DatabaseConfig.get_schema())
        cache_validator = SchemaValidator(CacheConfig.get_schema())
        security_validator = SchemaValidator(SecurityConfig.get_schema())
        
        # Create configurations with validators
        configs['application'] = ApplicationConfig(validator=app_validator)
        configs['database'] = DatabaseConfiguration(validator=db_validator)
        configs['cache'] = CacheConfiguration(validator=cache_validator)
        configs['security'] = SecurityConfiguration(validator=security_validator)
        configs['logging'] = LoggingConfiguration()
        configs['payment'] = PaymentConfiguration()
        configs['notification'] = NotificationConfiguration()
        configs['ppob'] = PPOBConfiguration()
        configs['monitoring'] = MonitoringConfiguration()
        configs['rate_limit'] = RateLimitConfiguration()
        configs['tasks'] = TaskConfiguration()
        
        return configs
    
    @staticmethod
    def create_with_loaders(config_dir: str = "config") -> Dict[str, BaseConfig]:
        """Create configurations with file and environment loaders"""
        configs = AppConfigFactory.create_all_configs()
        
        # Add loaders to each configuration
        for name, config in configs.items():
            # Add file loader
            file_loader = FileLoader()
            config._loader = file_loader
            
            # Add environment loader with prefix
            env_loader = EnvironmentLoader(f"{name.upper()}_")
            
            # Add memory cache
            cache = MemoryCache()
            config._cache = cache
        
        return configs
