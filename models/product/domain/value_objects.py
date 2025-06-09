from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from datetime import datetime

@dataclass(frozen=True)
class ProductCode:
    """Product code value object."""
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("Product code cannot be empty")

@dataclass(frozen=True)
class Price:
    """Price value object."""
    amount: Decimal
    currency: str = "IDR"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Price cannot be negative")
            
    def add_tax(self, percentage: Decimal) -> 'Price':
        """Add tax to price."""
        tax_amount = self.amount * (percentage / 100)
        return Price(self.amount + tax_amount, self.currency)