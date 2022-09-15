from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.deps import auth_user, get_session
from glossary.application.routes.schemas import HTTPErrorSchema
from glossary.application.routes.priority.schemas import ListPrioritySchema

from glossary.src.data.crud.holder import priority_crud


router = APIRouter(
    prefix="/priority",
    tags=["Priority"]
)

@router.get(
    "/list",
    responses={
        200: {"model": ListPrioritySchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def priority_list(
    _ = Depends(auth_user), 
    session: AsyncSession = Depends(get_session),
):
    priority_list = await priority_crud.get_many(
        session,
    )
    return ListPrioritySchema(items=priority_list)
