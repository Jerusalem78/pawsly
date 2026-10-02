from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated
from src.core.config import settings, debug
import uuid
from sqlalchemy import UUID
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=debug,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(primary_key=True)]
uuidpk = Annotated[uuid.UUID, mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
)]
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session