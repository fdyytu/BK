class Seller:
    """Seller base model."""

    def __init__(self, seller_id: int, name: str):
        self.seller_id = seller_id
        self.name = name