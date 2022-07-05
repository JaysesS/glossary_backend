from dataclasses import dataclass
from typing import Optional, Union
from glossary.src.core.entity.base import Tag
from glossary.src.core.dto.base import CreateTagDTO
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.result_base import Fail, Success

@dataclass
class SuccessResult(Success):
    item: Tag

@dataclass
class FailResult(Fail):
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self, 
        user_id: int,
        name: str,
        description: str
    ) -> Union[SuccessResult, FailResult]:

        tag = CreateTagDTO(
            name=name,
            description=description,
        )
        try:
            created_tag = self.repo.save_tag(tag=tag, user_id=user_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(item=created_tag)