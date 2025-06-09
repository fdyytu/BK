from typing import Dict, Any, Optional
from datetime import datetime
from .product import Product
from .category import Category
from .price import Price

class DigitalProduct(Product):
    """Digital product implementation."""
    
    def __init__(self,
                 name: str,
                 code: str,
                 category: Category,
                 price: Price,
                 provider: str,
                 digital_type: str,
                 expiry_period: Optional[int] = None):
        super().__init__(name, code, category, price)
        self.provider = provider
        self.digital_type = digital_type
        self.expiry_period = expiry_period  # in hours
        
    def get_details(self) -> Dict[str, Any]:
        """Get digital product details."""
        details = super().get_details()
        details.update({
            'provider': self.provider,
            'type': self.digital_type,
            'expiry_period': self.expiry_period
        })
        return details
    
    def validate(self) -> bool:
        """Validate digital product data."""
        return all([
            super().validate(),
            self.provider and len(self.provider.strip()) > 0,
            self.digital_type and len(self.digital_type.strip()) > 0,
            self.expiry_period is None or self.expiry_period > 0
        ])