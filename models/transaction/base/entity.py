class Entity:
    """Basic entity behavior."""

    def __init__(self, id: int):
        self.id = id

    def is_valid(self) -> bool:
        """Validate the entity."""
        return True