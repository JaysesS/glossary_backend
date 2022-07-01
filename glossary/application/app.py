from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from glossary.application.database.holder import db
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

    db.url = settings.DATABASE_URL
    db.make_engine()

    session = next(db.session)
    check, = session.execute('select 1').first()
    if check != 1:
        raise Exception("Problem with db on create_app")

    @app.exception_handler(AuthError)
    def auth_exception_handler(request: Request, exc: AuthError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)}
        )

    include_rotes(app, settings.GLOBAL_PREFIX_URL)

    return app