from typing import Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal

class BusinessMetrics:
    def __init__(self, db_connection):
        self.db = db_connection

    async def collect_transaction_metrics(self) -> Dict[str, Any]:
        """Collect transaction-related metrics"""
        now = datetime.utcnow()
        metrics = {
            "timestamp_utc": now.strftime('%Y-%m-%d %H:%M:%S'),
            "transactions": {
                "last_hour": await self._get_transaction_count(now - timedelta(hours=1)),
                "today": await self._get_transaction_count(now - timedelta(days=1)),
                "success_rate": await self._get_success_rate(),
                "average_amount": await self._get_average_amount(),
                "by_product_type": await self._get_transactions_by_product(),
                "by_payment_method": await self._get_transactions_by_payment_method()
            },
            "revenue": {
                "daily": await self._get_daily_revenue(),
                "weekly": await self._get_weekly_revenue(),
                "monthly": await self._get_monthly_revenue()
            },
            "users": {
                "active_today": await self._get_active_users(timedelta(days=1)),
                "active_weekly": await self._get_active_users(timedelta(days=7)),
                "new_today": await self._get_new_users(timedelta(days=1))
            }
        }
        return metrics

    async def _get_transaction_count(self, since: datetime) -> int:
        query = """
        SELECT COUNT(*) 
        FROM transactions 
        WHERE created_at >= $1
        """
        return await self.db.fetch_val(query, since)

    async def _get_success_rate(self) -> float:
        query = """
        SELECT 
            COUNT(CASE WHEN status = 'success' THEN 1 END)::float / 
            COUNT(*)::float * 100 as success_rate
        FROM transactions
        WHERE created_at >= NOW() - INTERVAL '1 day'
        """
        return await self.db.fetch_val(query)