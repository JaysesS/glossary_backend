from typing import List, Optional
from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from glossary.application.routes.schemas import WordSchema
from glossary.src.core.entity.base import User
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.word import save, list as uc_list, delete
from glossary.application.utils import auth_user, get_glossary_repo, reponse_from_result


router = APIRouter(
    prefix="/word",
    tags=["Word"],
)

class WordResponseSchema(BaseModel):
    item: WordSchema

class WordListResponseSchema(BaseModel):
    items: List[WordSchema]

class WordRemoveResponseSchema(BaseModel):
    remove_id: int

class WordCreateSchema(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=0)
    priority_id: int
    tag_ids: List[int]


@router.post("/", response_model=WordResponseSchema)
def save_word(
    word_data: WordCreateSchema = Body(),
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):
    usecase = save.Usecase(repo)
    result = usecase.execute(
        **word_data.dict(),
        user_id=user.id
    )

    model, code = reponse_from_result(WordResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )

@router.get("/list", response_model=WordListResponseSchema)
def list_word(
    offset: int = 0,
    limit: Optional[int] = None,
    priority_id: Optional[int] = None,
    tag_ids: Optional[str] = None,
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):
    if tag_ids is not None:
        try:
            tag_ids_list = list(map(int, tag_ids.split(","))) # type: ignore
        except Exception:
            return JSONResponse(content=dict(msg="Tag_ids must be like '1,2,3'"))
    else:
        tag_ids_list = None
    usecase = uc_list.Usecase(repo)
    result = usecase.execute(
        offset=offset,
        limit=limit,
        priority_id=priority_id,
        tag_ids=tag_ids_list,
        user_id=user.id
    )

    model, code = reponse_from_result(WordListResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )

@router.delete("/{id:int}", response_model=WordRemoveResponseSchema)
def rm_word(
    id: int,
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):

    usecase = delete.Usecase(repo)
    result = usecase.execute(
        word_id=id,
        user_id=user.id
    )
    model, code = reponse_from_result(WordRemoveResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )
