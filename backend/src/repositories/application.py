from src.repositories.base import BaseRepository
from src.models.application import ApplicationOrm
from src.models.listing import ListingOrm
from sqlalchemy import select,update as UPD
from sqlalchemy.orm import joinedload
from src.core.enums import ApplicationStatus
from typing import List
from uuid import UUID


class ApplicationRepository(BaseRepository[ApplicationOrm]):

    def __init__(self, session):
        super().__init__(session, ApplicationOrm)

    async def get_by_id(self, id: UUID) -> ApplicationOrm | None:
        result = await self.session.execute(
            select(ApplicationOrm)
            .where(ApplicationOrm.id == id)
            .options(
                joinedload(ApplicationOrm.listing).joinedload(ListingOrm.pet),
                joinedload(ApplicationOrm.sitter),
            )
        )
        return result.scalar_one_or_none()
        
    async def get_by_sitter_id(self, sitter_id : UUID, offset: int = 0, limit: int = 20) -> List[ApplicationOrm] | None:

        result = await self.session.execute(
            select(ApplicationOrm)
            .where(ApplicationOrm.sitter_id == sitter_id)
            .offset(offset)
            .limit(limit)
            .options(
                joinedload(ApplicationOrm.listing).joinedload(ListingOrm.pet),
                joinedload(ApplicationOrm.sitter),
            )
        )

        return result.scalars().all()
    
    async def get_by_listing_id(self, listing_id : UUID, offset: int = 0, limit: int = 20) -> List[ApplicationOrm] | None:

        result = await self.session.execute(
            select(ApplicationOrm)
            .where(ApplicationOrm.listing_id == listing_id)
            .offset(offset)
            .limit(limit)
            .options(
                joinedload(ApplicationOrm.listing).joinedload(ListingOrm.pet),
                joinedload(ApplicationOrm.sitter),
            )
        )

        return result.scalars().all()
    
    
    async def reject_all_except(self, listing_id: UUID, accepted_id: UUID) -> None:
        await self.session.execute(
            UPD(ApplicationOrm)
            .where(
                ApplicationOrm.listing_id == listing_id,
                ApplicationOrm.id != accepted_id,
                ApplicationOrm.status == ApplicationStatus.PENDING
            )
            .values(status=ApplicationStatus.REJECTED)
        )