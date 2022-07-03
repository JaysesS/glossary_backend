from dataclasses import dataclass
from typing import List, Union
from glossary.src.core.entity.base import Word
from glossary.src.core.dto.base import CreateWordDTO
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.result_base import Fail, Success

@dataclass
class SuccessResult(Success):
    item: Word

@dataclass
class FailResult(Fail):
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self, 
        user_id: int,
        name: str,
        description: str,
        tag_ids: List[int],
        priority_id: int
    ) -> Union[SuccessResult, FailResult]:
    
        word = CreateWordDTO(
            name=name,
            description=description,
            tag_ids=tag_ids,
            priority_id=priority_id,
        )

        try:
            created_word = self.repo.save_word(word, user_id=user_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(item=created_word)