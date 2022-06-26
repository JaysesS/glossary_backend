from fastapi import FastAPI
from glossary.application.routes.priority import priority
from glossary.application.routes.user import user

include = [
    priority.router,
    user.router,
]

def include_rotes(app: FastAPI, prefix: str = ""):
    for route in include:
        app.include_router(route, prefix=prefix)