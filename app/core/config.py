from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_origins: list[str]

def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv("DATABASE"),
        cors_origins=[os.getenv("CORE")],
    )