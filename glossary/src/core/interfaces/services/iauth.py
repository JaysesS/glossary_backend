from abc import ABC, abstractmethod


class IAuthService(ABC):

    secret: str
    lifetime: int

    @abstractmethod
    def generate_token(self, user_id: int) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass

    @abstractmethod
    def configure(self, secret: str, lifetime: int):
        pass