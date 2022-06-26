from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from glossary.application.database.holder import db
from glossary.src.data.repo.priority.repo import PriorityRepo
from glossary.src.core.usecases.priority import list

router = APIRouter(
    prefix="/priority",
    tags=["Priority"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@router.get("/list")
async def get_list():
    repo = PriorityRepo(session = next(db.session))
    usecase = list.Usecase(repo=repo)
    result = usecase.execute()
    return result