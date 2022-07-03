from dataclasses import dataclass
from typing import Union
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo

@dataclass
class SuccessResult:
    remove_id: int

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self, user_id: int, tag_id: int) -> Union[SuccessResult, FailResult]:
        try:
            removed_id = self.repo.rm_tag(id=tag_id, user_id=user_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(remove_id=removed_id)