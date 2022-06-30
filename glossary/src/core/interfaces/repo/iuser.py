from abc import ABC, abstractmethod
from typing import Optional
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import  User

class IUserRepo(ABC):

    @abstractmethod
    def save(self, user: CreateUserDTO) -> User:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find(self, name: str) -> Optional[User]:
        pass


