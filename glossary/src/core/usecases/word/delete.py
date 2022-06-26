from dataclasses import dataclass
from typing import Union
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iword import IWordRepo

@dataclass
class SuccessResult:
    remove_id: int 

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IWordRepo) -> None:
        self.repo = repo

    def execute(self, word_id: int) -> Union[SuccessResult, FailResult]:
        try:
            remove_id = self.repo.rm(word_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(remove_id=remove_id)