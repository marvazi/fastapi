import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_origins: list[str]


def get_settings() -> Settings:
    database_url = os.getenv("DATABASE")
    cors_origin = os.getenv("CORE")

    if database_url is None:
        raise RuntimeError("DATABASE is not configured")

    if cors_origin is None:
        raise RuntimeError("CORE is not configured")

    return Settings(
        DATABASE_URL=database_url,
        cors_origins=[cors_origin],
    )
