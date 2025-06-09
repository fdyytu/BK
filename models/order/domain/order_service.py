from typing import List
from uuid import UUID
from .order import Order
from .order_item import OrderItem
from .exceptions import OrderNotFoundError
from ..repositories import OrderRepository
from models.product.domain import Product
from models.product.repositories import ProductRepository

class OrderService:
    """Order domain service."""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository
    ):
        self._orders = order_repository
        self._products = product_repository
        
    async def create_order(
        self,
        buyer_id: UUID,
        product_ids: List[UUID],
        quantities: List[int]
    ) -> Order:
        """Create new order."""
        if len(product_ids) != len(quantities):
            raise ValueError("Product IDs and quantities must match")
            
        # Get products
        products = await self._products.get_many(product_ids)
        if len(products) != len(product_ids):
            raise ValueError("Some products not found")
            
        # Create order items
        items = [
            OrderItem(product, qty)
            for product, qty in zip(products, quantities)
        ]
        
        # Create and save order
        order = Order(buyer_id, items)
        return await self._orders.save(order)
        
    async def confirm_order(self, order_id: UUID) -> Order:
        """Confirm existing order."""
        order = await self._orders.get(order_id)
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")
            
        order.confirm()
        return await self._orders.save(order)