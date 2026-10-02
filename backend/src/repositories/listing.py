from src.repositories.base import BaseRepository
from src.models.listing import ListingOrm
from src.models.pet import PetsOrm
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.core.enums import Spicies
from datetime import datetime
from uuid import UUID


class ListingRepository(BaseRepository[ListingOrm]):

    def __init__(self, session):
        super().__init__(session, ListingOrm)

    async def get_by_owner_id(self, owner_id: UUID, offset: int = 0, limit: int = 20) -> list[ListingOrm]:
        result = await self.session.execute(
            select(ListingOrm)
            .offset(offset)
            .limit(limit)
            .where(ListingOrm.owner_id == owner_id)
            .options(joinedload(ListingOrm.owner))
        )
        return list(result.scalars().all())

    async def get_with_filters(
        self,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        species: Spicies | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        offset: int = 0,
        limit: int = 20
    ) -> list[ListingOrm]:
        filters = []

        if date_start:
            filters.append(ListingOrm.date_start >= date_start)
        if date_end:
            filters.append(ListingOrm.date_end <= date_end)
        if min_price is not None:
            filters.append(ListingOrm.price_per_day >= min_price)
        if max_price is not None:
            filters.append(ListingOrm.price_per_day <= max_price)

        query = (
            select(ListingOrm).
            offset(offset)
            .limit(limit)
            .join(ListingOrm.pet)
            .options(joinedload(ListingOrm.pet))
            .where(*filters)
        )

        if species:
            query = query.where(PetsOrm.spicies == species)

        result = await self.session.execute(query)
        return list(result.scalars().all())