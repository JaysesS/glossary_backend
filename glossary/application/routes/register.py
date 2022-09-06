from fastapi import FastAPI
from glossary.application.routes.schemas import HTTPErrorSchema
from glossary.application.routes.user import user
from glossary.application.routes.priority import priority
from glossary.application.routes.tag import tag
from glossary.application.routes.word import word

include = [
    user.router,
    priority.router,
    tag.router,
    word.router,
]

def include_rotes(app: FastAPI, prefix: str = ""):
    for route in include:
        app.include_router(
            route,
            prefix=prefix,
            responses={
                401: {"model": HTTPErrorSchema},
                403: {"model": HTTPErrorSchema},
                500: {"model": HTTPErrorSchema},
            }
        )