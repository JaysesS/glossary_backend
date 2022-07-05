from abc import ABC, abstractmethod
from glossary.src.core.entity.base import User
from glossary.src.core.interfaces.repo.iuser_sql_repo import IUserSQLRepo


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
    def login(self, name: str, password: str, repo: IUserSQLRepo) -> str:
        pass

    @abstractmethod
    def get_user_id(self, token) -> int:
        pass
    
    @abstractmethod
    def check(self, token: str, repo: IUserSQLRepo) -> User:
        pass