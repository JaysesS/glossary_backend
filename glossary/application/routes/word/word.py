from typing import List, Optional
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from glossary.application.routes.schemas import WordSchema
from glossary.src.core.entity.base import User
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.word import save, list, delete
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

class WordListSchema(BaseModel):
    offset: int = 0
    limit: Optional[int] = None
    priority_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


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

@router.post("/list", response_model=WordListResponseSchema)
def list_word(
    filter_data: WordListSchema = Body(),
    repo: IGlossarySQLRepo = Depends(get_glossary_repo),
    user: User = Depends(auth_user)
):
    usecase = list.Usecase(repo)
    result = usecase.execute(
        **filter_data.dict(),
        user_id=user.id
    )

    model, code = reponse_from_result(WordListResponseSchema, result)
    return JSONResponse(
        content=model.dict(),
        status_code=code
    )

@router.post("/{id:int}/delete", response_model=WordRemoveResponseSchema)
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
