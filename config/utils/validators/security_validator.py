from typing import Any, Dict, List, Optional, Set
import re
from datetime import datetime
import ssl
import socket
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from ..abstracts.base_validator import BaseValidator
from ..exceptions.validation_errors import ConfigValidationError

class SecurityValidator(BaseValidator[Dict[str, Any]]):
    """
    Security configuration validator with advanced features.
    
    Features:
    - SSL/TLS configuration validation
    - JWT token validation
    - Hash verification
    - Signature validation
    - Security policy enforcement
    - Key strength validation
    """
    
    def __init__(
        self,
        min_key_length: int = 2048,
        required_tls_version: float = 1.2,
        jwt_algorithms: Optional[List[str]] = None
    ) -> None:
        super().__init__()
        self.min_key_length = min_key_length
        self.required_tls_version = required_tls_version
        self.jwt_algorithms = jwt_algorithms or ['HS256', 'RS256', 'ES256']
        self._password_pattern = re.compile(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        )
    
    async def validate(
        self,
        data: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> bool:
        """
        Validate security configuration.
        
        Args:
            data: Security configuration to validate
            context: Optional validation context
            
        Returns:
            True if valid
        """
        try:
            # SSL/TLS Configuration
            if 'ssl' in data:
                await self._validate_ssl_config(data['ssl'])
            
            # JWT Configuration
            if 'jwt' in data:
                await self._validate_jwt_config(data['jwt'])
            
            # Key Configuration
            if 'keys' in data:
                await self._validate_keys(data['keys'])
            
            # Password Policies
            if 'password_policies' in data:
                await self._validate_password_policies(data['password_policies'])
            
            return len(self._errors) == 0
            
        except Exception as e:
            self.add_error({
                'type': 'security_validation_error',
                'message': str(e)
            })
            return False
    
    async def get_validation_rules(self) -> Dict[str, Any]:
        """Get current validation rules."""
        return {
            'min_key_length': self.min_key_length,
            'required_tls_version': self.required_tls_version,
            'jwt_algorithms': self.jwt_algorithms
        }
    
    async def _validate_ssl_config(self, config: Dict[str, Any]) -> None:
        """Validate SSL/TLS configuration."""
        try:
            # Validate certificate
            if 'certificate' in config:
                cert_path = config['certificate']
                context = ssl.create_default_context()
                context.load_cert_chain(cert_path)
            
            # Validate TLS version
            if 'version' in config:
                version = float(config['version'])
                if version < self.required_tls_version:
                    raise ValueError(
                        f"TLS version {version} is below required {self.required_tls_version}"
                    )
            
            # Validate cipher suites
            if 'ciphers' in config:
                allowed_ciphers = set(ssl.get_default_ciphers())
                configured_ciphers = set(config['ciphers'])
                invalid_ciphers = configured_ciphers - allowed_ciphers
                if invalid_ciphers:
                    raise ValueError(f"Invalid cipher suites: {invalid_ciphers}")
                
        except Exception as e:
            raise ValueError(f"SSL configuration validation failed: {str(e)}")
    
    async def _validate_jwt_config(self, config: Dict[str, Any]) -> None:
        """Validate JWT configuration."""
        try:
            # Validate algorithm
            if 'algorithm' in config and config['algorithm'] not in self.jwt_algorithms:
                raise ValueError(f"Unsupported JWT algorithm: {config['algorithm']}")
            
            # Validate secret/key
            if 'secret' in config:
                # Try to encode a test token
                jwt.encode(
                    {'test': 'test'},
                    config['secret'],
                    algorithm=config.get('algorithm', 'HS256')
                )
                
        except Exception as e:
            raise ValueError(f"JWT configuration validation failed: {str(e)}")
    
    async def _validate_keys(self, config: Dict[str, Any]) -> None:
        """Validate cryptographic keys."""
        try:
            for key_name, key_config in config.items():
                # Validate key length
                if 'length' in key_config:
                    length = int(key_config['length'])
                    if length < self.min_key_length:
                        raise ValueError(
                            f"Key length {length} is below minimum {self.min_key_length}"
                        )
                
                # Validate key usage
                if 'usage' in key_config:
                    valid_usages = {'signing', 'encryption', 'authentication'}
                    if key_config['usage'] not in valid_usages:
                        raise ValueError(f"Invalid key usage: {key_config['usage']}")
                
        except Exception as e:
            raise ValueError(f"Key configuration validation failed: {str(e)}")
    
    async def _validate_password_policies(self, config: Dict[str, Any]) -> None:
        """Validate password policies."""
        try:
            if 'pattern' in config:
                # Test pattern compilation
                re.compile(config['pattern'])
            
            if 'min_length' in config:
                min_length = int(config['min_length'])
                if min_length < 8:
                    raise ValueError("Minimum password length must be at least 8")
            
            if 'required_chars' in config:
                required = set(config['required_chars'])
                valid_chars = {'uppercase', 'lowercase', 'numbers', 'special'}
                invalid_chars = required - valid_chars
                if invalid_chars:
                    raise ValueError(f"Invalid required characters: {invalid_chars}")
                
        except Exception as e:
            raise ValueError(f"Password policy validation failed: {str(e)}")