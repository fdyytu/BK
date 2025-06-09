class Policy:
    """Access policies."""
    def __init__(self, policy_name, rules=None):
        self.policy_name = policy_name
        self.rules = rules or {}