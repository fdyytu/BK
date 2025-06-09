class AdminLog:
    """Admin activity logs."""

    def __init__(self, log_id: int, action: str):
        self.log_id = log_id
        self.action = action