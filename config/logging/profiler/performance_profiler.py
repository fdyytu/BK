import cProfile
import pstats
import io
from functools import wraps
from typing import Callable, Any
import logging

class PerformanceProfiler:
    def __init__(self):
        self.logger = logging.getLogger('performance')

    def profile(self, function_name: str = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                pr = cProfile.Profile()
                pr.enable()
                result = func(*args, **kwargs)
                pr.disable()
                
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                ps.print_stats(20)  # Top 20 time-consuming operations
                
                self.logger.info(
                    'Function performance profile',
                    extra={
                        'function_name': function_name or func.__name__,
                        'profile_data': s.getvalue(),
                        'timestamp_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    }
                )
                return result
            return wrapper
        return decorator