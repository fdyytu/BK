class Transaction:
    """Basic transaction behavior."""

    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id

    def process(self):
        """Process transaction logic."""
        pass