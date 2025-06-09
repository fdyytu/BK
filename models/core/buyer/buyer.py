from uuid import UUID
from typing import Optional
from models.core.base.entity import AggregateRoot
from .value_objects import Email, PhoneNumber
from .buyer_profile import BuyerProfile

class Buyer(AggregateRoot):
    """Buyer aggregate root."""
    
    def __init__(
        self,
        name: str,
        email: Email,
        phone: PhoneNumber,
        id: UUID = None
    ):
        super().__init__(id)
        self._name = name
        self._email = email
        self._phone = phone
        self._profile: Optional[BuyerProfile] = None
        
    def update_profile(self, profile: BuyerProfile) -> None:
        self._profile = profile
        self.update_timestamp()