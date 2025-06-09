class UserStatus:
    """User status management."""

    def __init__(self, status: str = "active"):
        self.status = status

    def deactivate(self):
        self.status = "inactive"

    def activate(self):
        self.status = "active"