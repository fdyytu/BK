from typing import Dict, Any
import requests
from datetime import datetime

class AlertManager:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.logger = logging.getLogger('alert')

    def send_alert(
        self,
        severity: str,
        title: str,
        description: str,
        **kwargs: Any
    ) -> None:
        """Send alerts to notification system"""
        alert_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'severity': severity,
            'title': title,
            'description': description,
            **kwargs
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=alert_data,
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f'Failed to send alert: {str(e)}', extra=alert_data)