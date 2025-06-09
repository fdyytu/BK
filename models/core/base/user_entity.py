class UserEntity:
    """Base user entity."""

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username