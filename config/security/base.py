from abc import ABC, abstractmethod

class AuthProvider(ABC):
    @abstractmethod
    def authenticate(self, credentials):
        pass

    @abstractmethod
    def get_user(self, token):
        pass

class SecurityPolicy(ABC):
    @abstractmethod
    def enforce(self, user, action, resource):
        pass