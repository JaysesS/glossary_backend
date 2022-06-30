from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import insert
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import User
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.iuser import IUserRepo
from glossary.src.data.repo.user.models import UserModel

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
        r = self.session.execute(stmt).scalar_one()
        try:
            self.session.commit()
        except Exception as err:
            raise RepoError(f"Error on save user") from err
        return User(id=r, name=user.name, password=user.password)

    def get(self, id: int) -> Optional[User]:
        return None

    def find(self, name: str) -> Optional[User]:
        return None