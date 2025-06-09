from typing import Any, Callable, Dict, List, Optional, Type, Union
from abc import ABC, abstractmethod
import logging
from datetime import datetime
import traceback

class ErrorContext:
    """Context information for errors."""
    
    def __init__(
        self,
        error: Exception,
        timestamp: datetime,
        location: str,
        user: str = "fdyytu",
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.timestamp = timestamp
        self.location = location
        self.user = user
        self.additional_info = additional_info or {}
        self.traceback = traceback.format_exc()

class ErrorHandler(ABC):
    """Abstract base class for error handlers following ISP."""
    
    @abstractmethod
    async def handle_error(self, context: ErrorContext) -> None:
        """Handle error with context."""
        pass

class LoggingErrorHandler(ErrorHandler):
    """Error handler that logs errors."""
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)
    
    async def handle_error(self, context: ErrorContext) -> None:
        """Log error with context."""
        error_msg = (
            f"Error occurred at {context.timestamp} in {context.location}\n"
            f"User: {context.user}\n"
            f"Error: {str(context.error)}\n"
            f"Additional Info: {context.additional_info}\n"
            f"Traceback:\n{context.traceback}"
        )
        self.logger.error(error_msg)

class NotificationErrorHandler(ErrorHandler):
    """Error handler that sends notifications."""
    
    def __init__(self, notification_service: Any) -> None:
        self.notification_service = notification_service
    
    async def handle_error(self, context: ErrorContext) -> None:
        """Send error notification."""
        await self.notification_service.send_alert(
            title=f"Error in {context.location}",
            message=str(context.error),
            severity="high",
            timestamp=context.timestamp,
            details=context.additional_info
        )

class CompositeErrorHandler(ErrorHandler):
    """Composite error handler following Composite pattern."""
    
    def __init__(self) -> None:
        self._handlers: List[ErrorHandler] = []
    
    def add_handler(self, handler: ErrorHandler) -> None:
        """Add error handler to composite."""
        self._handlers.append(handler)
    
    async def handle_error(self, context: ErrorContext) -> None:
        """Handle error with all registered handlers."""
        for handler in self._handlers:
            await handler.handle_error(context)

class ErrorHandlerFactory:
    """Factory for creating error handlers following Factory pattern."""
    
    @staticmethod
    def create_handler(
        handler_type: str,
        **kwargs: Any
    ) -> ErrorHandler:
        """Create error handler of specified type."""
        handlers = {
            'logging': LoggingErrorHandler,
            'notification': NotificationErrorHandler,
            'composite': CompositeErrorHandler
        }
        
        handler_class = handlers.get(handler_type)
        if not handler_class:
            raise ValueError(f"Unknown handler type: {handler_type}")
            
        return handler_class(**kwargs)

class ErrorHandlingService:
    """Service for handling errors following SRP."""
    
    def __init__(
        self,
        handler: ErrorHandler,
        error_filters: Optional[Dict[Type[Exception], bool]] = None
    ) -> None:
        self._handler = handler
        self._error_filters = error_filters or {}
        self._error_count: Dict[Type[Exception], int] = {}
    
    async def handle_error(
        self,
        error: Exception,
        location: str,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handle error if it passes filters."""
        # Check if error type should be handled
        if not self._should_handle_error(error):
            return
        
        # Create error context
        context = ErrorContext(
            error=error,
            timestamp=datetime.utcnow(),
            location=location,
            additional_info=additional_info
        )
        
        # Update error count
        error_type = type(error)
        self._error_count[error_type] = self._error_count.get(error_type, 0) + 1
        
        # Handle error
        await self._handler.handle_error(context)
    
    def add_error_filter(
        self,
        error_type: Type[Exception],
        should_handle: bool
    ) -> None:
        """Add filter for error type."""
        self._error_filters[error_type] = should_handle
    
    def get_error_count(
        self,
        error_type: Optional[Type[Exception]] = None
    ) -> Union[int, Dict[Type[Exception], int]]:
        """Get count of errors handled."""
        if error_type:
            return self._error_count.get(error_type, 0)
        return self._error_count.copy()
    
    def _should_handle_error(self, error: Exception) -> bool:
        """Check if error should be handled based on filters."""
        error_type = type(error)
        
        # Check specific error type
        if error_type in self._error_filters:
            return self._error_filters[error_type]
        
        # Check parent error types
        for base in error_type.__mro__[1:]:
            if base in self._error_filters:
                return self._error_filters[base]
        
        # Default to handling error
        return True