from glossary.application.settings import get_settings
from glossary.application.database.holder import db

settings = get_settings()

db.configure(url=settings.DATABASE_URL)