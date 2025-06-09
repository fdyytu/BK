from typing import Dict, Any, Optional
from datetime import datetime
import httpx
from .notification_interface import INotification
from ..common.exceptions import NotificationError

class NotificationBase(INotification):
    """Base class for notification implementations."""
    
    def __init__(self, 
                 api_key: str,
                 sender_id: str,
                 sandbox: bool = False):
        self.api_key = api_key
        self.sender_id = sender_id
        self.sandbox = sandbox
        self.base_url = self._get_base_url()
    
    def _get_base_url(self) -> str:
        """Get API base URL based on environment."""
        return f"https://{'sandbox' if self.sandbox else 'api'}.notifications.com/v1"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Sender-ID': self.sender_id,
            'Content-Type': 'application/json'
        }