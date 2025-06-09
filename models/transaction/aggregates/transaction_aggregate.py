class TransactionAggregate:
    """Transaction aggregate root."""
    def __init__(self, transaction_id, entities=None):
        self.transaction_id = transaction_id
        self.entities = entities or []