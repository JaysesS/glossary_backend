from dataclasses import dataclass
from typing import List, Optional, Union
from glossary.src.core.entity.base import Word
from glossary.src.core.dto.base import CreateWordDTO
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iword import IWordRepo
from glossary.src.core.interfaces.repo.itag import ITagRepo
from glossary.src.core.interfaces.repo.ipriority import IPriorityRepo

@dataclass
class SuccessResult:
    items: List[Word]

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IWordRepo) -> None:
        self.repo = repo

    def execute(self, limit: Optional[int] = None, offset: int = 0) -> Union[SuccessResult, FailResult]:

        try:
            word_list = self.repo.list(limit=limit, offset=offset)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(items=word_list)