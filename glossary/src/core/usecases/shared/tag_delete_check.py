from dataclasses import dataclass
from typing import Union
from glossary.src.core.entity.base import Tag
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.itag import ITagRepo
from glossary.src.core.interfaces.repo.iword import IWordRepo

@dataclass
class SuccessResult:
    tag: Tag
    count_words: int

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, tag_repo: ITagRepo, word_tepo: IWordRepo) -> None:
        self.tag_repo = tag_repo
        self.word_tepo = word_tepo

    def execute(self, tag_id: int) -> Union[SuccessResult, FailResult]:
        try:
            tag = self.tag_repo.get(id=tag_id)
        except RepoError as e:
            return FailResult(e.msg)
        
        try:
            count_words = len(self.word_tepo.list(tag_ids=[tag.id]))
        except RepoError as e:
            return FailResult(e.msg)

        return SuccessResult(tag=tag, count_words=count_words)