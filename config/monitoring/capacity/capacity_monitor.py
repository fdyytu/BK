from typing import Dict, Any
import numpy as np
from datetime import datetime, timedelta

class CapacityMonitor:
    def __init__(self, db_connection, config: Dict[str, Any]):
        self.db = db_connection
        self.config = config

    async def analyze_capacity(self) -> Dict[str, Any]:
        """Analyze system capacity and predict future needs"""
        current_metrics = await self._get_current_metrics()
        historical_data = await self._get_historical_data()
        
        return {
            "timestamp_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "current_capacity": current_metrics,
            "predictions": self._generate_predictions(historical_data),
            "recommendations": await self._generate_recommendations(current_metrics),
            "scaling_needs": await self._analyze_scaling_needs(historical_data)
        }

    async def _analyze_scaling_needs(self, historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze if system needs scaling"""
        return {
            "cpu_scaling": self._analyze_resource_scaling("cpu", historical_data),
            "memory_scaling": self._analyze_resource_scaling("memory", historical_data),
            "storage_scaling": self._analyze_resource_scaling("storage", historical_data),
            "network_scaling": self._analyze_resource_scaling("network", historical_data)
        }