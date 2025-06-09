class BaseModel:
    """Basic model attributes & common methods for all models."""

    def __init__(self, id: int = None):
        self.id = id

    def save(self):
        """Save the model to persistence."""
        pass

    def delete(self):
        """Delete the model from persistence."""
        pass