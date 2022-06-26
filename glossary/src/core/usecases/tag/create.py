from dataclasses import dataclass
from typing import Union
from glossary.src.core.entity.base import Tag
from glossary.src.core.dto.base import CreateTagDTO
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

    def execute(self, tag: CreateTagDTO) -> Union[SuccessResult, FailResult]:
        try:
            created_tag = self.repo.create(tag)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(tag=created_tag)