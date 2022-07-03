from dataclasses import dataclass
from typing import Union
from glossary.src.core.entity.base import Tag
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo

@dataclass
class SuccessResult:
    tag: Tag
    count_words: int

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, repo: IGlossarySQLRepo) -> None:
        self.repo = repo

    def execute(self, user_id: int, tag_id: int) -> Union[SuccessResult, FailResult]:
        try:
            tag = self.repo.get_tag(id=tag_id, user_id=user_id)
        except RepoError as e:
            return FailResult(e.msg)
        
        if tag is None:
            return FailResult("Tag not found")
        
        try:
            count_words = len(self.repo.list_word(user_id=user_id, tag_ids=[tag.id]))
        except RepoError as e:
            return FailResult(e.msg)

        return SuccessResult(tag=tag, count_words=count_words)