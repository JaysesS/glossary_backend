from sqlalchemy.orm import Session
from sqlalchemy import insert
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import User
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.ipriority import IPriorityRepo
from glossary.src.data.repo.user.models import UserModel

class UserRepo():

    def __init__(self, session: Session) -> None:
        self.session = session

    def register(self, user: CreateUserDTO) -> User:
        stmt = insert(
            UserModel
        ).values(
            name=user.name, password=user.password
        ).returning(
            UserModel.id
        )
        r = self.session.execute(stmt).scalar_one()
        self.session.commit()
        return User(id=r, name=user.name, password=user.password)