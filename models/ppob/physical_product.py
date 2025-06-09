from .product import Product

class PhysicalProduct(Product):
    """Physical product specifics."""

    def __init__(self, name: str, price: float, weight: float):
        super().__init__(name, price)
        self.weight = weight