class QueueConnectionError(Exception):
    """Raised when the queue connection fails."""
    pass

class QueuePublishError(Exception):
    """Raised when publishing a message fails."""
    pass

class QueueConsumeError(Exception):
    """Raised when consuming a message fails."""
    pass