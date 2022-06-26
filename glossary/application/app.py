from fastapi import FastAPI
from glossary.application.database.holder import db
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

    include_rotes(app, settings.GLOBAL_PREFIX_URL)

    

    return app