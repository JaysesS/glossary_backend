from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from glossary.src.core.dto.base import CreateTagDTO, UpdateTagDTO
from glossary.src.core.entity.base import Tag
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.itag import ITagRepo
from glossary.src.data.repo.models import TagModel

class TagRepo(ITagRepo):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, tag: CreateTagDTO) -> Tag:
        stmt = insert(
            TagModel
        ).values(
            name=tag.name, description=tag.description
        ).returning(
            TagModel.id
        )
        try:
            r = self.session.execute(stmt).scalar_one()
            self.session.commit()
        except Exception as err:
            raise RepoError(f"Error on save user") from err
        return Tag(id=r, name=tag.name, description=tag.description)

    def update(self, tag: UpdateTagDTO) -> Tag:
        pass

    def rm(self, id: int) -> int:
        pass

    def get(self, id: int) -> Tag:
        pass

    def list(self, ids: Optional[List[int]] = None, offset: int = 0, limit: Optional[int] = None) -> List[Tag]:
        pass