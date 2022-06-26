from dataclasses import dataclass
from typing import Union
from glossary.src.core.entity.base import Tag
from glossary.src.core.dto.base import UpdateTagDTO
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.itag import ITagRepo

@dataclass
class SuccessResult:
    tag: Tag

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: ITagRepo) -> None:
        self.repo = repo

    def execute(self, tag: UpdateTagDTO) -> Union[SuccessResult, FailResult]:
        try:
            update_tag = self.repo.update(tag)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(tag=update_tag)