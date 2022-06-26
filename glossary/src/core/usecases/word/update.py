from dataclasses import dataclass
from typing import Union
from glossary.src.core.entity.base import Word
from glossary.src.core.dto.base import UpdateWordDTO
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iword import IWordRepo
from glossary.src.core.interfaces.repo.itag import ITagRepo
from glossary.src.core.interfaces.repo.ipriority import IPriorityRepo

@dataclass
class SuccessResult:
    word: Word

@dataclass
class FailResult:
    msg: str

class Usecase:

    def __init__(self, word_repo: IWordRepo, tag_repo: ITagRepo, priority_repo: IPriorityRepo) -> None:
        self.word_repo = word_repo
        self.tag_repo = tag_repo
        self.priority_repo = priority_repo

    def execute(self, word: UpdateWordDTO) -> Union[SuccessResult, FailResult]:
        
        try:
            tags = self.tag_repo.list(ids=word.tag_ids)
        except RepoError as e:
            return FailResult(e.msg)
        
        if len(tags) != len(word.tag_ids):
            return FailResult(msg=f"One of tag not found: {word.tag_ids}")

        try:
            priority = self.priority_repo.get(id=word.priority_id)
        except RepoError as e:
            return FailResult(e.msg)

        try:
            updated_word = self.word_repo.update(word)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(word=updated_word)