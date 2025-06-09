from datetime import datetime
from typing import List, Optional
from uuid import UUID
from models.common.value_objects import Money
from models.common.base_entity import AggregateRoot
from .order_item import OrderItem
from .order_status import OrderStatus
from .exceptions import InvalidOrderState

class Order(AggregateRoot):
    """Order aggregate root."""
    
    def __init__(
        self,
        buyer_id: UUID,
        items: List[OrderItem],
        status: OrderStatus = OrderStatus.CREATED,
        id: UUID = None,
        created_at: datetime = None
    ):
        super().__init__(id)
        self._buyer_id = buyer_id
        self._items = items
        self._status = status
        self._created_at = created_at or datetime.utcnow()
        self._total = self._calculate_total()
        
    @property
    def total(self) -> Money:
        return self._total
        
    @property
    def status(self) -> OrderStatus:
        return self._status
        
    def add_item(self, item: OrderItem) -> None:
        """Add item to order."""
        if self._status != OrderStatus.CREATED:
            raise InvalidOrderState("Cannot modify confirmed order")
            
        self._items.append(item)
        self._total = self._calculate_total()
        
    def confirm(self) -> None:
        """Confirm order."""
        if self._status != OrderStatus.CREATED:
            raise InvalidOrderState("Order already confirmed")
            
        if not self._items:
            raise InvalidOrderState("Cannot confirm empty order")
            
        self._status = OrderStatus.CONFIRMED
        
    def _calculate_total(self) -> Money:
        return Money(
            sum(item.subtotal.amount for item in self._items),
            self._items[0].price.currency if self._items else "IDR"
        )