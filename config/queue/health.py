class QueueHealth:
    """
    Health check utility for queue providers.
    """
    def __init__(self, provider):
        self.provider = provider

    def ping(self) -> bool:
        try:
            # For demo: try connect and close (override for real provider)
            self.provider.connect()
            self.provider.close()
            return True
        except Exception:
            return False