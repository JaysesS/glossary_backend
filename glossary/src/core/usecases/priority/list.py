from dataclasses import dataclass
from typing import List, Union
from glossary.src.core.entity.base import Priority
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.ipriority import IPriorityRepo

@dataclass
class SuccessResult:
    items: List[Priority]

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IPriorityRepo) -> None:
        self.repo = repo

    def execute(self) -> Union[SuccessResult, FailResult]:
        try:
            priority_list = self.repo.list()
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(items=priority_list)