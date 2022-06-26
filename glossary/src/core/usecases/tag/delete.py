from dataclasses import dataclass
from typing import Union
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.itag import ITagRepo

@dataclass
class SuccessResult:
    remove_id: int

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: ITagRepo) -> None:
        self.repo = repo

    def execute(self, tag_id: int) -> Union[SuccessResult, FailResult]:
        try:
            removed_id = self.repo.rm(tag_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(remove_id=removed_id)