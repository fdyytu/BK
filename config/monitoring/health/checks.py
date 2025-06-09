from typing import Dict, Any
import aiohttp
import asyncpg
import aioredis
from datetime import datetime

class HealthChecker:
    def __init__(
        self,
        db_pool: asyncpg.Pool,
        redis: aioredis.Redis,
        external_services: Dict[str, str]
    ):
        self.db_pool = db_pool
        self.redis = redis
        self.external_services = external_services

    async def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        return {
            "timestamp_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "healthy",  # Will be updated based on checks
            "checks": {
                "database": await self._check_database(),
                "redis": await self._check_redis(),
                "external_services": await self._check_external_services(),
                "disk_space": await self._check_disk_space(),
                "memory": await self._check_memory(),
                "background_workers": await self._check_background_workers()
            }
        }

    async def _check_database(self) -> Dict[str, Any]:
        try:
            start_time = datetime.utcnow()
            async with self.db_pool.acquire() as conn:
                await conn.execute('SELECT 1')
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time * 1000, 2)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }