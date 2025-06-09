class DomainEvent:
    """Base class for domain events."""

    def __init__(self, name: str, payload: dict):
        self.name = name
        self.payload = payload