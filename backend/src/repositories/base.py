from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, Generic
from uuid import UUID

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session : AsyncSession, model : Type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id : UUID) -> T | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, offset: int = 0, limit: int = 20) -> list[T]:
        result = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, **kwargs) -> T:
        result = await self.session.execute(
            insert(self.model).values(**kwargs).returning(self.model)
        )
        return result.scalar_one()
    
    async def update(self, id : UUID, **kwargs) -> T:
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        return result.scalar_one_or_none()
    
    async def delete(self, id : UUID) -> T | None:
        result = await self.session.execute(
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model)
        )
        return result.scalar_one_or_none()