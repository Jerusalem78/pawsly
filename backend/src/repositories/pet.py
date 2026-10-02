from src.repositories.base import BaseRepository
from src.models.pet import PetsOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID


class PetsRepository(BaseRepository[PetsOrm]):

    def __init__(self, session):
        super().__init__(session, PetsOrm)

    async def get_by_owner_id(self, owner_id: UUID, offset: int = 0, limit: int = 20) -> list[PetsOrm] | None:

        result = await self.session.execute(
            select(PetsOrm).where(PetsOrm.owner_id == owner_id).offset(offset).limit(limit).options(selectinload(PetsOrm.owner))
        )

        return result.scalars().all()
