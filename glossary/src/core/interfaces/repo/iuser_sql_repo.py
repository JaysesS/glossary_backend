from abc import ABC, abstractmethod
from typing import Optional
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import User

class IUserSQLRepo(ABC):

    @abstractmethod
    def save_user(self, user: CreateUserDTO) -> User:
        pass

    @abstractmethod
    def get_user(self, id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_user(self, login: str) -> Optional[User]:
        pass