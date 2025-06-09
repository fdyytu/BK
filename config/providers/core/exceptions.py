class ProviderError(Exception):
    """Base exception for provider errors"""
    pass

class AuthenticationError(ProviderError):
    """Raised when provider authentication fails"""
    pass

class ValidationError(ProviderError):
    """Raised when request validation fails"""
    pass

class ConnectionError(ProviderError):
    """Raised when provider connection fails"""
    pass

class TransactionError(ProviderError):
    """Raised when transaction processing fails"""
    pass

class InquiryError(ProviderError):
    """Raised when inquiry fails"""
    pass

class BalanceError(ProviderError):
    """Raised when balance check fails"""
    pass