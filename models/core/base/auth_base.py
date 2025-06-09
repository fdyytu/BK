from abc import ABC, abstractmethod
from typing import Optional

class AuthenticationBase(ABC):
    """Base class for authentication."""
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate user."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate authentication."""
        pass