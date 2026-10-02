from src.repositories.base import BaseRepository
from src.models.dispute import DisputeOrm
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.core.enums import DisputeStatus
from typing import List
from uuid import UUID

class DisputeRepository(BaseRepository[DisputeOrm]):

    def __init__(self, session):
        super().__init__(session, DisputeOrm)

    async def get_by_booking_id(self, booking_id: UUID) -> DisputeOrm | None:
    
        result = await self.session.execute(
            select(DisputeOrm).where(DisputeOrm.booking_id == booking_id).options(joinedload(DisputeOrm.booking))
        )

        return result.scalar_one_or_none()
    
    async def get_open_disputes(self, offset: int = 0, limit: int = 20) -> List[DisputeOrm] | None:

        result = await self.session.execute(
            select(DisputeOrm).where(DisputeOrm.status == DisputeStatus.OPEN).offset(offset).limit(limit)
        )

        return result.scalars().all()