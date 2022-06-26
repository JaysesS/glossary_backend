from dataclasses import dataclass
from typing import List, Union
from glossary.src.core.entity.base import Word
from glossary.src.core.dto.base import CreateWordDTO
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

    def execute(self, name: str, description: str, tag_id_list: List[int], priority_id: int) -> Union[SuccessResult, FailResult]:
        
        try:
            tags = self.tag_repo.list(ids=tag_id_list)
        except RepoError as e:
            return FailResult(e.msg)

        try:
            priority = self.priority_repo.get(id=priority_id)
        except RepoError as e:
            return FailResult(e.msg)

        word = CreateWordDTO(
            name=name,
            description=description,
            tags=tags,
            priority=priority
        )

        try:
            created_word = self.word_repo.create(word)
        except RepoError as e:
            return FailResult(e.msg)
        return SuccessResult(word=created_word)