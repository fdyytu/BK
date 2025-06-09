from datetime import datetime
from typing import Optional

class RateLimitLogger:
    def __init__(self):
        self.logger = logging.getLogger('rate_limit')

    def log_rate_limit_event(
        self,
        user_id: str,
        endpoint: str,
        limit: int,
        remaining: int,
        reset_time: datetime,
        ip_address: Optional[str] = None
    ) -> None:
        """Log rate limit events"""
        rate_limit_data = {
            'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': user_id,
            'endpoint': endpoint,
            'limit': limit,
            'remaining': remaining,
            'reset_time': reset_time.strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': ip_address
        }
        
        self.logger.warning('Rate limit reached', extra=rate_limit_data)