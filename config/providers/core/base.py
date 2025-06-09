from typing import Dict, Any, Optional
import aiohttp
import json
import logging
from datetime import datetime
from .interfaces import BaseProvider
from .exceptions import (
    ProviderError,
    AuthenticationError,
    ValidationError,
    ConnectionError,
    TransactionError
)

class BaseProviderImpl:
    """Base implementation for providers"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        api_secret: str,
        timeout: int = 30
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self.session

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to provider"""
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        start_time = datetime.utcnow()
        
        try:
            async with session.request(
                method,
                url,
                json=data,
                params=params,
                headers=headers or {}
            ) as response:
                response_data = await response.json()
                
                # Log response time
                elapsed = (datetime.utcnow() - start_time).total_seconds()
                self.logger.info(
                    f"Provider request completed",
                    extra={
                        "provider": self.__class__.__name__,
                        "method": method,
                        "endpoint": endpoint,
                        "response_time": elapsed,
                        "status_code": response.status
                    }
                )
                
                # Handle errors
                if not str(response.status).startswith('2'):
                    raise ProviderError(
                        f"Provider error: {response_data.get('message', 'Unknown error')}"
                    )
                    
                return response_data
                
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ProviderError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}")

    async def _validate_signature(self, data: Dict[str, Any]) -> bool:
        """Validate webhook signature"""
        raise NotImplementedError("Signature validation not implemented")

    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None