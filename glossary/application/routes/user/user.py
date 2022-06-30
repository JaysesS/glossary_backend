from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from glossary.application.database.holder import db
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.usecases.priority import list
from glossary.src.data.repo.user.repo import UserRepo

router = APIRouter(
    prefix="/user",
    tags=["User"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# @router.get("/me")
# async def me():
#     repo = PriorityRepo(session = next(db.session))
#     usecase = list.Usecase(repo=repo)
#     result = usecase.execute()
#     return result

@router.post("/register")
async def register():
    repo = UserRepo(session = next(db.session))
    print(repo.save(CreateUserDTO(name="shrek", password="123")))
    return 123
    
# @router.post("/login")
# async def login():
#     repo = PriorityRepo(session = next(db.session))
#     usecase = list.Usecase(repo=repo)
#     result = usecase.execute()
#     return result