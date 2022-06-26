from abc import ABC, abstractmethod
from typing import List, Optional

from glossary.src.core.dto.base import CreateWordDTO, UpdateWordDTO
from glossary.src.core.entity.base import Word

class IWordRepo(ABC):
    
    @abstractmethod
    def create(self, word: CreateWordDTO) -> Word:
        pass
    
    @abstractmethod
    def update(self, word: UpdateWordDTO) -> Word:
        pass
    
    @abstractmethod
    def rm(self, id: int) -> int:
        pass

    @abstractmethod
    def list(self, tag_ids: Optional[List[int]] = None, offset: int = 0, limit: Optional[int] = None) -> List[Word]:
        pass