from typing import List, Optional
from datetime import datetime
from models.core.base.entity import AggregateRoot
from .value_objects import ProductCode, Price
from .category import Category

class Product(AggregateRoot):
    """Product aggregate root."""
    
    def __init__(
        self, 
        code: ProductCode,
        name: str,
        base_price: Price,
        category: Category,
        id: UUID = None
    ):
        super().__init__(id)
        self._code = code
        self._name = name
        self._base_price = base_price
        self._category = category
        self._is_active = True
        
    @property
    def code(self) -> ProductCode:
        return self._code
        
    @property
    def price(self) -> Price:
        return self._base_price
        
    def activate(self) -> None:
        """Activate the product."""
        self._is_active = True
        self.update_timestamp()
        
    def deactivate(self) -> None:
        """Deactivate the product."""
        self._is_active = False
        self.update_timestamp()