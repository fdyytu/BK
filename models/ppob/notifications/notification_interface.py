from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class INotification(ABC):
    """Interface for notification implementations."""
    
    @abstractmethod
    async def send(self, 
                  recipient: str,
                  template_id: str,
                  data: Dict[str, Any]) -> bool:
        """Send notification to recipient."""
        pass
    
    @abstractmethod
    async def get_status(self, notification_id: str) -> Dict[str, Any]:
        """Get notification status."""
        pass