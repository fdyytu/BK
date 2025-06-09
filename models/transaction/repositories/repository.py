class Repository:
    """Base repository pattern."""

    def add(self, entity):
        raise NotImplementedError

    def get(self, entity_id):
        raise NotImplementedError

    def remove(self, entity):
        raise NotImplementedError