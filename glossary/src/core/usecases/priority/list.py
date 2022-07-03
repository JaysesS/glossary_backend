from dataclasses import dataclass
from typing import List, Union
from glossary.src.core.entity.base import Priority
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.result_base import Fail, Success

@dataclass
class SuccessResult(Success):
    items: List[Priority]

@dataclass
class FailResult(Fail):
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self) -> Union[SuccessResult, FailResult]:
        try:
            priority_list = self.repo.list_priority()
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(items=priority_list)