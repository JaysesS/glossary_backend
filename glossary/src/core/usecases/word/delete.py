from dataclasses import dataclass
from typing import Union
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.result_base import Fail, Success

@dataclass
class SuccessResult(Success):
    remove_id: int 

@dataclass
class FailResult(Fail):
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self, user_id: int, word_id: int) -> Union[SuccessResult, FailResult]:
        try:
            remove_id = self.repo.rm_word(user_id=user_id, id=word_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(remove_id=remove_id)