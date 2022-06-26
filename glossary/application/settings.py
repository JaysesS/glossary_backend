from functools import lru_cache
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "GLOSSATY APP"
    GLOBAL_PREFIX_URL: str = "/api/v1"

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_HOST", "5432")
    DB_USER: str = os.getenv("DB_USER", "jayse")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "test")
    DB_NAME: str = os.getenv("DB_NAME", "glossary_app_db")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()