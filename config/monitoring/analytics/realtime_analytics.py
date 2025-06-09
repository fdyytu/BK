from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta
import pandas as pd

class RealtimeAnalytics:
    def __init__(self, redis_client, db_connection):
        self.redis = redis_client
        self.db = db_connection
        self.metrics_window = 300  # 5 minutes

    async def get_realtime_metrics(self) -> Dict[str, Any]:
        """Get real-time business metrics"""
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=self.metrics_window)
        
        metrics = {
            "timestamp_utc": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "transactions": await self._get_realtime_transactions(window_start),
            "revenue": await self._get_realtime_revenue(window_start),
            "active_users": await self._get_active_users(window_start),
            "error_rates": await self._get_error_rates(window_start),
            "product_performance": await self._get_product_metrics(window_start),
            "system_health": await self._get_system_health()
        }

        await self._store_historical_metrics(metrics)
        return metrics

    async def get_trend_analysis(self) -> Dict[str, Any]:
        """Analyze trends in real-time data"""
        historical_data = await self._get_historical_metrics()
        df = pd.DataFrame(historical_data)
        
        return {
            "trends": {
                "transaction_trend": self._calculate_trend(df['transactions']),
                "revenue_trend": self._calculate_trend(df['revenue']),
                "user_trend": self._calculate_trend(df['active_users'])
            },
            "anomalies": self._detect_anomalies(df),
            "predictions": await self._generate_predictions(df)
        }