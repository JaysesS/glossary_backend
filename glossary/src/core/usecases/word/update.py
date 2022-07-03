from dataclasses import dataclass
from typing import Optional, Union, List
from glossary.src.core.entity.base import Word
from glossary.src.core.dto.base import UpdateWordDTO
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
        word_id: int,
        description: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
        priority_id: Optional[int] = None
    ) -> Union[SuccessResult, FailResult]:
        
        update_word = UpdateWordDTO(
            id=word_id,
            description=description,
            tag_ids=tag_ids,
            priority_id=priority_id
        )

        try:
            updated_word = self.repo.update_word(update_word, user_id=user_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(item=updated_word)