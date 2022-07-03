from abc import ABC, abstractmethod
from typing import List, Optional
from glossary.src.core.entity.base import Priority, User, Tag, Word
from glossary.src.core.dto.base import CreatePriorityDTO, CreateTagDTO, CreateUserDTO, CreateWordDTO, UpdateTagDTO, UpdateWordDTO

class IGlossarySQLRepo(ABC):

    @abstractmethod
    def save_priority(self, priority: CreatePriorityDTO) -> Priority:
        pass

    @abstractmethod
    def get_priority(self, id: int) -> Priority:
        pass
    
    @abstractmethod
    def list_priority(self) -> List[Priority]:
        pass
    
    @abstractmethod
    def save_tag(self, tag: CreateTagDTO, user_id: int) -> Tag:
        pass

    @abstractmethod
    def update_tag(self, tag: UpdateTagDTO, user_id: int) -> Tag:
        pass

    @abstractmethod
    def rm_tag(self, id: int, user_id: int) -> int:
        pass

    @abstractmethod
    def get_tag(self, id: int, user_id: int) -> Optional[Tag]:
        pass

    @abstractmethod
    def list_tag(self,
        user_id: int,
        ids: Optional[List[int]] = None,
        offset: int = 0,
        limit: Optional[int] = None
    ) -> List[Tag]:
        pass

    @abstractmethod
    def save_user(self, user: CreateUserDTO) -> User:
        pass

    @abstractmethod
    def get_user(self, id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_user(self, name: str) -> Optional[User]:
        pass

    @abstractmethod
    def save_word(self, word: CreateWordDTO, user_id: int) -> Word:
        pass
    
    @abstractmethod
    def update_word(self, word: UpdateWordDTO, user_id: int) -> Word:
        pass
    
    @abstractmethod
    def rm_word(self, id: int, user_id: int) -> int:
        pass

    @abstractmethod
    def list_word(self, 
        user_id: int,
        tag_ids: Optional[List[int]] = None,
        offset: int = 0,
        limit: Optional[int] = None
    ) -> List[Word]:
        pass
