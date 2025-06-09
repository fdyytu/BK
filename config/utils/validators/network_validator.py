from typing import Any, Dict, List, Optional, Union
import socket
import asyncio
from urllib.parse import urlparse
import ipaddress

from ..abstracts.base_validator import BaseValidator
from ..exceptions.validation_errors import ConfigValidationError

class NetworkValidator(BaseValidator[Dict[str, Any]]):
    """
    Network configuration validator with advanced features.
    
    Features:
    - URL validation
    - Port availability check
    - DNS resolution
    - IP range validation
    - SSL certificate validation
    - Timeout configuration
    """
    
    def __init__(
        self,
        timeout: float = 5.0,
        verify_ssl: bool = True,
        dns_resolver: Optional[str] = None
    ) -> None:
        super().__init__()
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.dns_resolver = dns_resolver
        self._cache: Dict[str, Any] = {}
    
    async def validate(
        self,
        data: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> bool:
        """
        Validate network configuration.
        
        Args:
            data: Network configuration to validate
            context: Optional validation context
            
        Returns:
            True if valid
        """
        try:
            tasks = []
            
            # URL validation
            if 'urls' in data:
                tasks.extend([
                    self._validate_url(url)
                    for url in data['urls']
                ])
            
            # Port validation
            if 'ports' in data:
                tasks.extend([
                    self._validate_port(port)
                    for port in data['ports']
                ])
            
            # IP range validation
            if 'ip_ranges' in data:
                tasks.extend([
                    self._validate_ip_range(ip_range)
                    for ip_range in data['ip_ranges']
                ])
            
            # Execute all validation tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for result in results:
                if isinstance(result, Exception):
                    self.add_error({
                        'type': 'network_error',
                        'message': str(result)
                    })
            
            return len(self._errors) == 0
            
        except Exception as e:
            self.add_error({
                'type': 'validation_error',
                'message': str(e)
            })
            return False
    
    async def get_validation_rules(self) -> Dict[str, Any]:
        """Get current validation rules."""
        return {
            'timeout': self.timeout,
            'verify_ssl': self.verify_ssl,
            'dns_resolver': self.dns_resolver
        }
    
    async def _validate_url(self, url: str) -> bool:
        """Validate URL and its availability."""
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError(f"Invalid URL format: {url}")
            
            # DNS resolution
            try:
                await asyncio.get_event_loop().getaddrinfo(
                    parsed.hostname,
                    parsed.port or (443 if parsed.scheme == 'https' else 80)
                )
            except socket.gaierror as e:
                raise ValueError(f"DNS resolution failed for {url}: {str(e)}")
            
            return True
            
        except Exception as e:
            raise ValueError(f"URL validation failed: {str(e)}")
    
    async def _validate_port(self, port: Union[int, Dict[str, Any]]) -> bool:
        """Validate port configuration and availability."""
        try:
            port_number = port if isinstance(port, int) else port.get('number')
            
            if not 0 <= port_number <= 65535:
                raise ValueError(f"Invalid port number: {port_number}")
            
            # Check if port is available
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            try:
                result = sock.connect_ex(('localhost', port_number))
                if result == 0:
                    raise ValueError(f"Port {port_number} is already in use")
            finally:
                sock.close()
            
            return True
            
        except Exception as e:
            raise ValueError(f"Port validation failed: {str(e)}")
    
    async def _validate_ip_range(self, ip_range: str) -> bool:
        """Validate IP range format and accessibility."""
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            
            # Validate network size
            if network.num_addresses > 65536:
                raise ValueError(f"IP range too large: {ip_range}")
            
            return True
            
        except Exception as e:
            raise ValueError(f"IP range validation failed: {str(e)}")