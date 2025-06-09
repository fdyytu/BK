from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from models.core.base.entity import AggregateRoot
from .order_item import OrderItem
from .order_status import OrderStatus
from .payment_details import PaymentDetails

class Order(AggregateRoot):
    """Order aggregate root."""
    
    def __init__(
        self, 
        buyer_id: UUID,
        items: List[OrderItem],
        id: UUID = None
    ):
        super().__init__(id)
        self._buyer_id = buyer_id
        self._items = items
        self._status = OrderStatus.CREATED
        self._total_amount = self._calculate_total()
        self._payment: Optional[PaymentDetails] = None
        
    def _calculate_total(self) -> Decimal:
        return sum(item.subtotal for item in self._items)
        
    def add_item(self, item: OrderItem) -> None:
        if self._status != OrderStatus.CREATED:
            raise ValueError("Cannot modify confirmed order")
        self._items.append(item)
        self._total_amount = self._calculate_total()
        
    def confirm_payment(self, payment: PaymentDetails) -> None:
        if self._status != OrderStatus.CREATED:
            raise ValueError("Order already processed")
        self._payment = payment
        self._status = OrderStatus.PAID