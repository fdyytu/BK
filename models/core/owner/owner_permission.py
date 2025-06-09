class OwnerPermission:
    """Owner permissions."""
    def __init__(self, permissions=None):
        self.permissions = permissions or []