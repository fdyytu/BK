class UnitOfWork:
    """Unit of Work pattern to manage atomic transactions."""

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass