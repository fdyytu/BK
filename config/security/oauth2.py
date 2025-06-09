class OAuth2Provider:
    def __init__(self, client_id, client_secret, provider_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.provider_url = provider_url

    def get_authorize_url(self):
        # Return authorization URL
        pass

    def fetch_token(self, code):
        # Exchange code for access token
        pass

    def get_user_info(self, token):
        # Fetch user info from provider
        pass