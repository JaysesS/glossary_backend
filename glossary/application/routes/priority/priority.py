from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from glossary.application.routes.schemas import PriorirySchema

from glossary.src.core.entity.base import User
from glossary.application.utils import get_glossary_repo, auth_user, reponse_from_result
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.priority import list

router = APIRouter(
    prefix="/priority",
    tags=["Priority"],
)

class PrioriryListResponseSchema(BaseModel):
    items: List[PriorirySchema]

@router.get("/list", response_model=PrioriryListResponseSchema)
async def get_list(
    repo: IGlossarySQLRepo = Depends(get_glossary_repo)
):
    usecase = list.Usecase(repo=repo)
    result = usecase.execute()
    model, code = reponse_from_result(PrioriryListResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )