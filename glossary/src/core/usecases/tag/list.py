from dataclasses import dataclass
from typing import Optional, Union, List
from glossary.src.core.entity.base import Tag
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo

@dataclass
class SuccessResult:
    items: List[Tag]

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self, user_id: int, offset: int = 0, limit: Optional[int] = None) -> Union[SuccessResult, FailResult]:
        try:
            tags = self.repo.list_tag(user_id=user_id, offset=offset, limit=limit)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(items=tags)