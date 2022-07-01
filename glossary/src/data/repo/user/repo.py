from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import User
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iuser import IUserRepo
from glossary.src.data.repo.models import UserModel

class UserRepo(IUserRepo):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, user: CreateUserDTO) -> User:
        stmt = insert(
            UserModel
        ).values(
            name=user.name, password=user.password
        ).returning(
            UserModel.id
        )
        try:
            r = self.session.execute(stmt).scalar_one()
            self.session.commit()
        except Exception as err:
            raise RepoError("Error on save user") from err
        return User(id=r, name=user.name, password=user.password)

    def get(self, id: int) -> Optional[User]:
        try:
            r = self.session.query(UserModel).get(id)
        except Exception:
            raise RepoError("Error on get user")
        if not r:
            return None
        return User(id=r.id, name=r.name, password=r.password)

    def find(self, name: str) -> Optional[User]:
        stmt = select(UserModel)
        stmt = stmt.where(
            UserModel.name == name
        )
        r = self.session.execute(stmt).scalar()
        if not r:
            return None
        return User(id=r.id, name=r.name, password=r.password)