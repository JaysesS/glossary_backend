from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import User
from glossary.src.core.exception.base import RepoError
from glossary.src.data.user_repo.models import UserModel
from glossary.src.core.interfaces.repo.iuser_sql_repo import IUserSQLRepo


class UserSQLRepo(IUserSQLRepo):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_user(self, user: CreateUserDTO) -> User:
        user_model = UserModel(
            login=user.login, password=user.password
        )
        self.session.add(user_model)
        try:
            self.session.commit()
        except Exception as err:
            raise RepoError("Error on save user") from err
        return User(
            id=user_model.id, # type: ignore
            login=user.login,
            password=user.password,
            created_at=int(user_model.created_at.timestamp())
        )

    def get_user(self, id: int) -> Optional[User]:
        try:
            r = self.session.query(UserModel).get(id)
        except Exception:
            raise RepoError("Error on get user")
        if not r:
            return None
        return User(id=r.id, login=r.name, password=r.password, created_at=int(r.created_at.timestamp()))

    def find_user(self, login: str) -> Optional[User]:
        stmt = select(UserModel)
        stmt = stmt.where(
            UserModel.login == login
        )
        r = self.session.execute(stmt).scalar()
        if not r:
            return None
        return User(id=r.id, login=r.login, password=r.password, created_at=int(r.created_at.timestamp()))