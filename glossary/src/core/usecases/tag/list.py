from dataclasses import dataclass
from typing import Optional, Union, List
from glossary.src.core.entity.base import Tag
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.itag import ITagRepo

@dataclass
class SuccessResult:
    items: List[Tag]

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: ITagRepo) -> None:
        self.repo = repo

    def execute(self, offset: int = 0, limit: Optional[int] = None) -> Union[SuccessResult, FailResult]:
        try:
            tags = self.repo.list(offset=offset, limit=limit)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(items=tags)