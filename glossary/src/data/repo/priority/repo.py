from typing import List
from sqlalchemy.orm import Session
from glossary.src.core.entity.base import Priority
from glossary.src.core.exception.base import RepoError
from glossary.src.core.interfaces.repo.ipriority import IPriorityRepo
from glossary.src.data.repo.models import PriorityModel

class PriorityRepo(IPriorityRepo):

    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, id: int) -> Priority:
        r = self.session.query(PriorityModel).get(id)
        if not r:
            raise RepoError(f"Priority with {id=} not found")
        return Priority(id=r.id, name=r.name)
    
    def list(self) -> List[Priority]:
        lst = self.session.query(PriorityModel).all()
        return [
            Priority(id=r.id, name=r.name)
            for r in lst
        ]