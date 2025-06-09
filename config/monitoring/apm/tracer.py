from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from typing import Dict, Any

class APMTracer:
    def __init__(self, service_name: str, config: Dict[str, Any]):
        self.service_name = service_name
        self.config = config
        self._setup_tracer()

    def _setup_tracer(self) -> None:
        tracer_provider = TracerProvider()
        jaeger_exporter = JaegerExporter(
            agent_host_name=self.config["jaeger_host"],
            agent_port=self.config["jaeger_port"],
        )
        tracer_provider.add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
        trace.set_tracer_provider(tracer_provider)
        self.tracer = trace.get_tracer(self.service_name)

    async def trace_operation(self, operation_name: str, **kwargs: Any) -> None:
        with self.tracer.start_as_current_span(operation_name) as span:
            span.set_attribute("service.name", self.service_name)
            for key, value in kwargs.items():
                span.set_attribute(key, str(value))