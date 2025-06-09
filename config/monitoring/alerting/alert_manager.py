from typing import Dict, Any, List
from datetime import datetime
import asyncio
from .channels.slack import SlackNotifier
from .channels.email import EmailNotifier
from .channels.sms import SMSNotifier

class AlertManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.slack = SlackNotifier(config['slack_webhook_url'])
        self.email = EmailNotifier(config['smtp_config'])
        self.sms = SMSNotifier(config['sms_config'])
        
        # Alert history for deduplication
        self.alert_history: Dict[str, datetime] = {}
        
        # Alert suppression windows
        self.suppression_windows: Dict[str, datetime] = {}

    async def process_alert(
        self,
        alert_type: str,
        severity: str,
        message: str,
        metadata: Dict[str, Any]
    ) -> None:
        """Process and distribute alerts based on rules"""
        alert_id = f"{alert_type}:{metadata.get('source', 'unknown')}"
        
        if self._is_alert_suppressed(alert_id):
            return

        if self._should_deduplicate(alert_id):
            return

        channels = self._get_channels_for_severity(severity)
        alert_tasks = []

        for channel in channels:
            if channel == 'slack':
                alert_tasks.append(self.slack.send_alert(severity, message, metadata))
            elif channel == 'email':
                alert_tasks.append(self.email.send_alert(severity, message, metadata))
            elif channel == 'sms':
                alert_tasks.append(self.sms.send_alert(severity, message, metadata))

        await asyncio.gather(*alert_tasks)
        self._update_alert_history(alert_id)

    def _is_alert_suppressed(self, alert_id: str) -> bool:
        """Check if alert is currently suppressed"""
        if alert_id in self.suppression_windows:
            if datetime.utcnow() < self.suppression_windows[alert_id]:
                return True
        return False

    def _should_deduplicate(self, alert_id: str) -> bool:
        """Check if alert should be deduplicated"""
        if alert_id in self.alert_history:
            last_alert_time = self.alert_history[alert_id]
            if (datetime.utcnow() - last_alert_time).total_seconds() < self.config['dedup_window']:
                return True
        return False

    def _get_channels_for_severity(self, severity: str) -> List[str]:
        """Get notification channels based on severity"""
        return self.config['severity_channels'].get(severity, ['slack'])

    def _update_alert_history(self, alert_id: str) -> None:
        """Update alert history for deduplication"""
        self.alert_history[alert_id] = datetime.utcnow()