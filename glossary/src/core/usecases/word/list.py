from dataclasses import dataclass
from typing import List, Optional, Union
from glossary.src.core.entity.base import Word
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.result_base import Fail, Success

@dataclass
class SuccessResult(Success):
    items: List[Word]

@dataclass
class FailResult(Fail):
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self,
        user_id: int,
        priority_id: Optional[int] = None, # TODO
        tag_ids: Optional[List[int]] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> Union[SuccessResult, FailResult]:

        try:
            word_list = self.repo.list_word(user_id=user_id, tag_ids=tag_ids, limit=limit, offset=offset)
        except RepoError as e:
            return FailResult(e.msg)
        
        return SuccessResult(items=word_list)