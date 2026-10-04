from src.repositories.base import BaseRepository
from src.models.booking import BookingOrm
from src.models.listing import ListingOrm
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import List
from uuid import UUID

class BookingRepository(BaseRepository[BookingOrm]):

    def __init__(self, session):
        super().__init__(session, BookingOrm)

    async def get_by_id(self, id: UUID) -> BookingOrm | None:
        result = await self.session.execute(
            select(BookingOrm)
            .where(BookingOrm.id == id)
            .options(
                joinedload(BookingOrm.listing).joinedload(ListingOrm.pet),
                joinedload(BookingOrm.owner),
                joinedload(BookingOrm.sitter),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_owner_id(self, owner_id: UUID, offset: int = 0, limit: int = 20) -> List[BookingOrm] | None:
        result = await self.session.execute(
            select(BookingOrm)
            .where(BookingOrm.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
            .options(
                joinedload(BookingOrm.listing).joinedload(ListingOrm.pet),
                joinedload(BookingOrm.owner),
                joinedload(BookingOrm.sitter),
            )
        )

        return result.scalars().all()
    
    async def get_by_sitter_id(self, sitter_id: UUID, offset: int = 0, limit: int = 20) -> List[BookingOrm] | None:
        result = await self.session.execute(
            select(BookingOrm)
            .where(BookingOrm.sitter_id == sitter_id)
            .offset(offset)
            .limit(limit)
            .options(
                joinedload(BookingOrm.listing).joinedload(ListingOrm.pet),
                joinedload(BookingOrm.owner),
                joinedload(BookingOrm.sitter),
            )
        )

        return result.scalars().all()
    
    async def get_by_listing_id(self, listing_id: UUID) -> BookingOrm | None:
        result = await self.session.execute(
            select(BookingOrm)
            .where(BookingOrm.listing_id == listing_id)
            .options(
                joinedload(BookingOrm.listing).joinedload(ListingOrm.pet),
                joinedload(BookingOrm.owner),
                joinedload(BookingOrm.sitter),
            )
        )

        return result.scalar_one_or_none()
    
