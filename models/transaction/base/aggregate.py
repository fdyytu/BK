class AggregateRoot:
    """Aggregate root behavior for DDD."""

    def __init__(self, id: int):
        self.id = id
        self._entities = []

    def add_entity(self, entity):
        self._entities.append(entity)