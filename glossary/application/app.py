from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from glossary.application.settings import get_settings
from glossary.application.database.holder import db
from glossary.application.routes.register import include_rotes
from glossary.application.utils.error_handlers import register_error_handlers

from glossary.src.core.exception.base import AuthError
from glossary.src.core.services.jwt_auth import auth_service


def create_app():
    settings = get_settings()
    app = FastAPI(
        title=settings.TITLE,
        docs_url=f"{settings.GLOBAL_PREFIX_URL}/docs",
        redoc_url=f"{settings.GLOBAL_PREFIX_URL}/redoc",
        debug=True
    )
    app.add_middleware(
    CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    db.configure(settings.DATABASE_URL)

    auth_service.configure(
        secret=settings.SECRET_KEY,
        lifetime=settings.TOKEN_LIFE_TIME
    )

    include_rotes(app, settings.GLOBAL_PREFIX_URL)
    register_error_handlers(app)

    return app