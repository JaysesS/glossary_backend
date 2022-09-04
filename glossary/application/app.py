from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from glossary.application.database.holder import db
from glossary.application.utils import init_debug_validation_handler
from glossary.src.core.exception.base import AuthError
from glossary.application.settings import get_settings
from glossary.application.routes.register import include_rotes


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

    @app.exception_handler(AuthError)
    def auth_exception_handler(request: Request, exc: AuthError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(Exception)
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Unhandled error!"}
        )

    include_rotes(app, settings.GLOBAL_PREFIX_URL)
    init_debug_validation_handler(app)

    return app