class GameServiceException(Exception):
    """Base exception for game service."""
    pass

class GameValidationError(GameServiceException):
    """Raised when game validation fails."""
    pass

class InsufficientBalanceError(GameServiceException):
    """Raised when service balance is insufficient."""
    pass

class TransactionError(GameServiceException):
    """Raised when transaction processing fails."""
    pass

class MonitoringError(GameServiceException):
    """Raised when transaction monitoring fails."""
    pass