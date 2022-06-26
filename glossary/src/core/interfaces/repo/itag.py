from abc import ABC, abstractmethod
from typing import List, Optional
from glossary.src.core.dto.base import CreateTagDTO, UpdateTagDTO

from glossary.src.core.entity.base import Tag

class ITagRepo(ABC):

    @abstractmethod
    def create(self, tag: CreateTagDTO) -> Tag:
        pass

    @abstractmethod
    def update(self, tag: UpdateTagDTO) -> Tag:
        pass

    @abstractmethod
    def rm(self, id: int) -> int:
        pass

    @abstractmethod
    def get(self, id: int) -> Tag:
        pass

    @abstractmethod
    def list(self, ids: Optional[List[int]] = None, offset: int = 0, limit: Optional[int] = None) -> List[Tag]:
        pass
