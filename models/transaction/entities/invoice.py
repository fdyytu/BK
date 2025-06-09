class Invoice:
    """Invoice."""

    def __init__(self, invoice_id: str, order_id: str):
        self.invoice_id = invoice_id
        self.order_id = order_id