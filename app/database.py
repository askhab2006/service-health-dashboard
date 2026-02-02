from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .config import settings
from fastapi import Depends
from typing import Annotated

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

new_session = async_sessionmaker(
    engine,
    class_=AsyncSession, 
    expire_on_commit=False
    )

class Base(DeclarativeBase):
    pass

async def get_db():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
