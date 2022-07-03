from dataclasses import dataclass
from typing import Optional, Union
from glossary.src.core.entity.base import Tag
from glossary.src.core.dto.base import UpdateTagDTO
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo

@dataclass
class SuccessResult:
    tag: Tag

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self,
        user_id: int,
        tag_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Union[SuccessResult, FailResult]:

        tag_update = UpdateTagDTO(
            id=tag_id,
            name=name,
            description=description
        )

        try:
            update_tag = self.repo.update_tag(tag_update, user_id=user_id)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(tag=update_tag)