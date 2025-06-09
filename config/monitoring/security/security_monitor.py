from typing import Dict, Any, List
from datetime import datetime
import asyncio
import json

class SecurityMonitor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alert_manager = AlertManager(config['alert_config'])
        self.threat_patterns = self._load_threat_patterns()

    async def monitor_security_events(self) -> None:
        """Monitor security-related events"""
        while True:
            events = await self._collect_security_events()
            threats = self._analyze_threats(events)
            
            if threats:
                await self._handle_threats(threats)
            
            await asyncio.sleep(self.config['security_check_interval'])

    async def _collect_security_events(self) -> List[Dict[str, Any]]:
        """Collect security events from various sources"""
        return await asyncio.gather(
            self._check_failed_logins(),
            self._check_api_abuse(),
            self._check_suspicious_transactions(),
            self._check_system_modifications()
        )

    def _analyze_threats(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze events for potential security threats"""
        threats = []
        for event in events:
            for pattern in self.threat_patterns:
                if self._match_threat_pattern(event, pattern):
                    threats.append({
                        "timestamp_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        "type": pattern["type"],
                        "severity": pattern["severity"],
                        "event": event,
                        "pattern_matched": pattern["name"]
                    })
        return threats