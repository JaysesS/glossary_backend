from abc import ABC, abstractmethod
from glossary.src.core.interfaces.repo.iuser import IUserRepo


class IAuthService(ABC):

    secret: str
    lifetime: int

    @abstractmethod
    def _generate_token(self, user_id: int) -> str:
        pass

    @abstractmethod
    def _verify_token(self, token: str) -> int:
        pass

    @abstractmethod
    def login(self, name: str, password: str, repo: IUserRepo) -> str:
        pass
    
    @abstractmethod
    def check(self, token: str, repo: IUserRepo) -> bool:
        pass