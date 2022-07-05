from typing import List, Optional
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from glossary.application.routes.schemas import TagSchema
from glossary.src.core.entity.base import User
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.tag import save, list as uc_list, delete
from glossary.application.utils import auth_user, get_glossary_repo, reponse_from_result


router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
)

class TagResponseSchema(BaseModel):
    item: TagSchema

class TagListResponseSchema(BaseModel):
    items: List[TagSchema]

class TagRemoveResponseSchema(BaseModel):
    remove_id: int

class TagCreateSchema(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=0)

@router.post("/", response_model=TagResponseSchema)
def save_tag(
    tag_data: TagCreateSchema = Body(),
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):
    usecase = save.Usecase(repo)
    result = usecase.execute(
        **tag_data.dict(),
        user_id=user.id
    )
    model, code = reponse_from_result(TagResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )

@router.get("/list", response_model=TagListResponseSchema)
def list_tag(
    offset: int = 0,
    limit: Optional[int] = None,
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):
    usecase = uc_list.Usecase(repo)
    result = usecase.execute(
        offset=offset,
        limit=limit,
        user_id=user.id
    )

    model, code = reponse_from_result(TagListResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )

@router.delete("/{id:int}", response_model=TagRemoveResponseSchema)
def rm_tag(
    id: int,
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):
    usecase = delete.Usecase(repo)
    result = usecase.execute(
        tag_id=id,
        user_id=user.id
    )
    model, code = reponse_from_result(TagRemoveResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )