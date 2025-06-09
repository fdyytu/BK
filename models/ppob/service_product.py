from .product import Product

class ServiceProduct(Product):
    """Service product specifics."""

    def __init__(self, name: str, price: float, duration: int):
        super().__init__(name, price)
        self.duration = duration  # duration in days/hours