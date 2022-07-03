from typing import List, Optional
from sqlalchemy import delete, insert, select, and_
from sqlalchemy.orm import Session
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.exception.base import RepoError
from glossary.src.core.dto.base import CreateTagDTO, CreateUserDTO,CreateWordDTO,  UpdateTagDTO, UpdateWordDTO, CreatePriorityDTO
from glossary.src.core.entity.base import Priority, Tag, Word, User
from glossary.src.data.repo.models import UserModel, WordModel, TagModel, WordTagModel, PriorityModel

class GlossarySQLRepo(IGlossarySQLRepo):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_priority(self, priority: CreatePriorityDTO) -> Priority:
        stmt = insert(
            PriorityModel
        ).values(
            name=priority.name
        ).returning(
            PriorityModel.id
        )
        try:
            r = self.session.execute(stmt).scalar_one()
            self.session.commit()
        except Exception as err:
            raise RepoError(f"Error on save priority") from err
        return Priority(id=r, name=priority.name)

    def get_priority(self, id: int) -> Priority:
        r = self.session.query(PriorityModel).get(id)
        if not r:
            raise RepoError(f"Priority with {id=} not found")
        return Priority(id=r.id, name=r.name)
    
    def list_priority(self) -> List[Priority]:
        lst = self.session.query(PriorityModel).all()
        return [
            Priority(id=r.id, name=r.name)
            for r in lst
        ]
    
    def save_tag(self, tag: CreateTagDTO,  user_id: int) -> Tag:
        tag_model = TagModel(
            name=tag.name,
            description=tag.description,
            user_id=user_id
        )
        self.session.add(tag_model)
        try:
            self.session.commit()
        except Exception as err:
            raise RepoError(f"Error on save tag") from err
        return Tag(id=tag_model.id, name=tag.name, description=tag.description, created_at=int(tag_model.created_at.timestamp()))

    def update_tag(self, tag: UpdateTagDTO, user_id: int) -> Tag:
        pass

    def rm_tag(self, id: int, user_id: int) -> int:
        stmt = delete(TagModel).where(
            TagModel.id == id,
            TagModel.user_id == user_id
        ).returning(
            TagModel.id
        )
        try:
            r = self.session.execute(stmt).scalar_one()
        except Exception:
            raise RepoError("Error on rm tag")
        return r

    def get_tag(self, id: int, user_id: int) -> Optional[Tag]:
        try:
            r = self.session.query(TagModel).get(id)
        except Exception:
            raise RepoError("Error on get tag")
        if not r or r.user_id != user_id:
            return None
        return Tag(id=r.id, name=r.name, description=r.description, created_at=int(r.created_at.timestamp()))

    def list_tag(self,
        user_id: int,
        ids: Optional[List[int]] = None,
        offset: int = 0,
        limit: Optional[int] = None
    ) -> List[Tag]:
        stmt = select(
            TagModel
        )
        where_condition = [
            TagModel.user_id == user_id
        ]
        if isinstance(ids, list):
            where_condition.append(
                TagModel.id.in_(ids)
            )
        stmt = stmt.where(
            and_(*where_condition)
        )
        stmt = stmt.offset(offset)
        if isinstance(limit, int):
            stmt = stmt.limit(limit)
        try:
            rt = self.session.execute(stmt).scalars().all()
        except Exception as err:
            raise RepoError(f"Error on list tag") from err
        
        return [
            Tag(id=t.id, name=t.name, description=t.description, created_at=int(t.created_at.timestamp()))
            for t in rt
        ]

    def save_user(self, user: CreateUserDTO) -> User:
        user_model = UserModel(
            name=user.name, password=user.password
        )
        self.session.add(user_model)
        try:
            self.session.commit()
        except Exception as err:
            raise RepoError("Error on save user") from err
        return User(id=user_model.id, name=user.name, password=user.password, created_at=int(user_model.created_at.timestamp()))

    def get_user(self, id: int) -> Optional[User]:
        try:
            r = self.session.query(UserModel).get(id)
        except Exception:
            raise RepoError("Error on get user")
        if not r:
            return None
        return User(id=r.id, name=r.name, password=r.password, created_at=int(r.created_at.timestamp()))

    def find_user(self, name: str) -> Optional[User]:
        stmt = select(UserModel)
        stmt = stmt.where(
            UserModel.name == name
        )
        r = self.session.execute(stmt).scalar()
        if not r:
            return None
        return User(id=r.id, name=r.name, password=r.password, created_at=int(r.created_at.timestamp()))

    def save_word(self, word: CreateWordDTO, user_id: int) -> Word:
        tags_stmt = select(TagModel).where(TagModel.id.in_(word.tag_ids))
        try:
            tag_models = self.session.execute(tags_stmt).scalars().all()
        except Exception as err:
            raise RepoError(f"Error on save word") from err
        
        if len(tag_models) != len(word.tag_ids):
            raise RepoError("Some tags not found")

        try:
            priority_model = self.session.query(PriorityModel).get(word.priority_id)
        except Exception:
            raise RepoError("Error on save word")
        if not priority_model:
            raise RepoError("Priority not found")

        word_model = WordModel(
            name=word.name,
            description=word.description,
            priority_id=word.priority_id,
            user_id=user_id
        )
        self.session.add(word_model)

        try:
            self.session.flush()
        except Exception as err:
            raise RepoError(f"Error on save word") from err

        for tag_model in tag_models:
            wt_model = WordTagModel(
                word_id=word_model.id,
                tag_id=tag_model.id
            )
            self.session.add(wt_model)

        try:
            self.session.commit()
        except Exception as err:
            raise RepoError(f"Error on save word") from err
        
        tags_entity = [
            Tag(id=t.id, name=t.name, description=t.description, created_at=int(t.created_at.timestamp()))
            for t in word_model.tags
        ]
        priority_entity = Priority(
            id=priority_model.id,
            name=priority_model.name
        )
        return Word(
            id=word_model.id, # type: ignore
            name=word.name,
            description=word.description,
            tags=tags_entity,
            priority=priority_entity,
            created_at=int(word_model.created_at.timestamp()) # type: ignore
        )
    
    def update_word(self, word: UpdateWordDTO, user_id: int) -> Word:
        pass
    
    def rm_word(self, id: int, user_id: int) -> int:
        stmt = delete(WordModel).where(
            and_(
                WordModel.id == id,
                WordModel.user_id == user_id
            )
        )
        stmt = stmt.returning(
            WordModel.id
        )
        try:
            r = self.session.execute(stmt).scalar_one()
        except Exception:
            raise RepoError("Error on rm word")
        return r

    def list_word(self, 
        user_id: int,
        tag_ids: Optional[List[int]] = None,
        offset: int = 0,
        limit: Optional[int] = None
    ) -> List[Word]:
        stmt = select(
            WordModel
        )

        if isinstance(user_id, int):
            stmt = stmt.where(
                WordModel.user_id == user_id
            )
        
        if isinstance(tag_ids, list):
            stmt = stmt.join(
                WordTagModel, WordModel.id == WordTagModel.word_id
            ).where(
                WordTagModel.tag_id.in_(tag_ids)
            ).group_by(
                WordModel.id
            )
        
        stmt = stmt.offset(offset)

        if isinstance(limit, int):
            stmt = stmt.limit(limit)

        stmt = stmt.order_by(WordModel.created_at.desc())

        try:
            rw = self.session.execute(stmt).scalars().all()
        except Exception as err:
            raise RepoError(f"Error on list word") from err

        return [
            Word(
                id=word_model.id,
                name=word_model.name,
                description=word_model.description,
                created_at=int(word_model.created_at.timestamp()),
                tags=[
                    Tag(
                        id=tag.id,
                        name=tag.name,
                        description=tag.description,
                        created_at=int(tag.created_at.timestamp())
                    )
                    for tag in word_model.tags
                ],
                priority=Priority(
                    id=word_model.priority.id,
                    name=word_model.priority.name
                )
            )
            for word_model in rw
        ]
