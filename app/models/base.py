from uuid import uuid4
from sqlalchemy import String
from sqlalchemy.orm import mapped_column,Mapped,DeclarativeBase



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String, primary_key=True,default=lambda: str(uuid4()))
