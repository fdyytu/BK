from typing import Optional

class DomainError(Exception):
    """Base exception for domain errors."""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "DOMAIN_ERROR"
        super().__init__(message)

class BusinessError(DomainError):
    """Business rule violation."""
    pass

class ValidationError(DomainError):
    """Data validation error."""
    pass

class NotFoundError(DomainError):
    """Entity not found."""
    pass

class InfrastructureError(Exception):
    """Base exception for infrastructure errors."""
    pass