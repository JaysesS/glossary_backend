from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.database.holder import db

async def get_session() -> AsyncSession: # type: ignore
    async with db.session() as session: # type: ignore
        yield session

