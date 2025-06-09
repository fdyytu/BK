from typing import Dict, Any, Optional, List
from datetime import datetime
from .notification_interface import INotification
from .sms_notification import SMSNotification
from .email_notification import EmailNotification
from .push_notification import PushNotification
from ..common.exceptions import NotificationError

class NotificationService:
    """Service for managing notifications."""
    
    def __init__(self, config: Dict[str, Dict[str, str]]):
        self.config = config
        self.services: Dict[str, INotification] = {}
        self._initialize_services()
    
    def _initialize_services(self) -> None:
        """Initialize notification services."""
        if 'sms' in self.config:
            self.services['sms'] = SMSNotification(
                api_key=self.config['sms']['api_key'],
                sender_id=self.config['sms']['sender_id'],
                sandbox=self.config['sms'].get('sandbox', False)
            )
            
        if 'email' in self.config:
            self.services['email'] = EmailNotification(
                api_key=self.config['email']['api_key'],
                sender_id=self.config['email']['sender_id'],
                sandbox=self.config['email'].get('sandbox', False)
            )
            
        if 'push' in self.config:
            self.services['push'] = PushNotification(
                api_key=self.config['push']['api_key'],
                sender_id=self.config['push']['sender_id'],
                sandbox=self.config['push'].get('sandbox', False)
            )
    
    async def send_notification(self,
                              notification_type: str,
                              recipient: str,
                              template_id: str,
                              data: Dict[str, Any]) -> bool:
        """Send notification."""
        service = self.services.get(notification_type)
        
        if not service:
            raise NotificationError(
                f"Unsupported notification type: {notification_type}"
            )
            
        return await service.send(recipient, template_id, data)
    
    async def send_multi_channel(self,
                               channels: List[str],
                               recipient: Dict[str, str],
                               template_ids: Dict[str, str],
                               data: Dict[str, Any]) -> Dict[str, bool]:
        """Send notification through multiple channels."""
        results = {}
        
        for channel in channels:
            if channel not in self.services:
                results[channel] = False
                continue
                
            try:
                results[channel] = await self.send_notification(
                    channel,
                    recipient.get(channel, ''),
                    template_ids.get(channel, ''),
                    data
                )
            except Exception:
                results[channel] = False
                
        return results
    
    async def get_status(self,
                        notification_type: str,
                        notification_id: str) -> Dict[str, Any]:
        """Get notification status."""
        service = self.services.get(notification_type)
        
        if not service:
            raise NotificationError(
                f"Unsupported notification type: {notification_type}"
            )
            
        return await service.get_status(notification_id)