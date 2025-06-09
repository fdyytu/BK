from typing import Dict, Any, Optional
from datetime import datetime
from .notification_base import NotificationBase
from ..common.exceptions import NotificationError

class SMSNotification(NotificationBase):
    """SMS notification implementation."""
    
    async def send(self,
                  recipient: str,
                  template_id: str,
                  data: Dict[str, Any]) -> bool:
        """Send SMS notification."""
        try:
            endpoint = f"{self.base_url}/sms/send"
            headers = self._get_headers()
            
            payload = {
                'to': recipient,
                'template_id': template_id,
                'data': data,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    raise NotificationError(
                        f"Failed to send SMS: {response.text}"
                    )
                    
                return True
                
        except Exception as e:
            raise NotificationError(f"SMS notification failed: {str(e)}")
    
    async def get_status(self, notification_id: str) -> Dict[str, Any]:
        """Get SMS notification status."""
        endpoint = f"{self.base_url}/sms/status/{notification_id}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                endpoint,
                headers=headers
            )
            
            if response.status_code != 200:
                raise NotificationError(
                    f"Failed to get status: {response.text}"
                )
                
            return response.json()