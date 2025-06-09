from config.logging import (
    LoggerSetup,
    TracingContext,
    PerformanceProfiler,
    AuditLogger,
    IntegrationLogger,
    CacheLogger,
    TaskLogger,
    AlertManager
)

# Setup loggers
logger_setup = LoggerSetup(env='production')
audit_logger = AuditLogger()
perf_profiler = PerformanceProfiler()
integration_logger = IntegrationLogger()
cache_logger = CacheLogger()
task_logger = TaskLogger()
alert_manager = AlertManager(webhook_url='https://alerts.example.com/webhook')

# Contoh penggunaan dalam API endpoint
@perf_profiler.profile()
async def process_payment(payment_data: Dict[str, Any]) -> Dict[str, Any]:
    trace_context = TracingContext()
    start_time = time.time()
    
    try:
        # Log audit trail
        audit_logger.log_data_access(
            user_id=payment_data['user_id'],
            action='payment_initiation',
            resource_type='payment',
            resource_id=payment_data['payment_id'],
            changes=payment_data
        )
        
        # Check cache
        cache_key = f"payment:{payment_data['payment_id']}"
        cache_start = time.time()
        cached_data = await cache.get(cache_key)
        cache_logger.log_cache_operation(
            operation='get',
            key=cache_key,
            success=cached_data is not None,
            execution_time=time.time() - cache_start
        )
        
        # External service call
        gateway_start = time.time()
        payment_result = await payment_gateway.process(payment_data)
        integration_logger.log_external_request(
            service='payment_gateway',
            endpoint='/process',
            method='POST',
            status_code=payment_result['status_code'],
            response_time=time.time() - gateway_start,
            payment_id=payment_data['payment_id']
        )
        
        # Background task
        task_id = str(uuid4())
        task_logger.log_task_execution(
            task_id=task_id,
            task_name='payment_notification',
            status='scheduled',
            execution_time=0,
            payment_id=payment_data['payment_id']
        )
        
        return {
            'status': 'success',
            'payment_id': payment_data['payment_id'],
            'trace_id': trace_context.get_context()['trace_id']
        }
        
    except Exception as e:
        # Send alert for critical errors
        alert_manager.send_alert(
            severity='critical',
            title='Payment Processing Failed',
            description=str(e),
            payment_id=payment_data['payment_id'],
            user_id=payment_data['user_id']
        )
        raise
    finally:
        # Log overall execution time
        execution_time = time.time() - start_time
        if execution_time > 5.0:  # Threshold for slow operations
            alert_manager.send_alert(
                severity='warning',
                title='Slow Payment Processing',
                description=f'Payment processing took {execution_time:.2f} seconds',
                payment_id=payment_data['payment_id']
            )