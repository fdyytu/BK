from opentelemetry import trace
from typing import Optional, Dict, Any
import time

class TracingContext:
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)

    def get_context(self) -> Dict[str, str]:
        current_span = trace.get_current_span()
        context = {
            'trace_id': format(current_span.get_span_context().trace_id, '032x'),
            'span_id': format(current_span.get_span_context().span_id, '016x'),
        }
        return context