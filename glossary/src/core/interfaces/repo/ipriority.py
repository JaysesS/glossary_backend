from abc import ABC, abstractmethod
from typing import List

from glossary.src.core.entity.base import Priority

class IPriorityRepo(ABC):

    @abstractmethod
    def get(self, id: int) -> Priority:
        pass
    
    @abstractmethod
    def list(self) -> List[Priority]:
        pass