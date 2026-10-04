from src.repositories.listing import ListingRepository
from src.repositories.pet import PetsRepository
from src.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.listing import ListingUpdateSchemas, ListingPostSchema
from uuid import UUID
from src.core.enums import ListingStatus
from src.core.state_machine import LISTING_TRANSITION, validate_transition

class ListingService:

    def __init__(self, session):
        self.listing_repo =  ListingRepository(session)
        self.pet_repo = PetsRepository(session)
        self.session : AsyncSession = session 

    async def __check_if_own_listing(self, listing_id: UUID, user_id: UUID):
        listing = await self.listing_repo.get_by_id(listing_id)
        
        if not listing:
            raise NotFoundException("Листинг не найден")
        
        if listing.owner_id != user_id:
            raise ForbiddenException("Не ваш листинг")

    async def create_listing(self, user_id : UUID, data : ListingPostSchema):

        pet = await self.pet_repo.get_by_id(data.pet_id)

        if not pet:
            raise NotFoundException("Питомец не найден")

        if user_id != pet.owner_id:
            raise BadRequestException("Это не ваш питомец")

        if data.date_start >= data.date_end:
            raise BadRequestException("date_end должен быть позже date_start")

        listing = await self.listing_repo.create(
                owner_id=user_id,
                pet_id=data.pet_id,
                date_start=data.date_start,
                date_end=data.date_end,
                price_per_day=data.price_per_day,
                description=data.description,
        )

        await self.session.commit()

        refreshed_listing = await self.listing_repo.get_by_id(listing.id)
        return refreshed_listing

    async def get_listing(
        self,
        offset: int = 0,
        limit: int = 20,
        date_start=None,
        date_end=None,
        spicies=None,
        min_price=None,
        max_price=None,
    ):
        listing = await self.listing_repo.get_with_filters(
            offset=offset,
            limit=limit,
            date_start=date_start,
            date_end=date_end,
            species=spicies,
            min_price=min_price,
            max_price=max_price,
        )
        return listing
    async def get_my_listing(self, user_id : UUID,  offset: int = 0, limit: int = 20):
        listing = await self.listing_repo.get_by_owner_id(owner_id=user_id, limit=limit, offset=offset)
        return listing

    async def get_listing_by_id(self, listing_id: UUID):
        listing = await self.listing_repo.get_by_id(listing_id)

        if not listing:
            raise NotFoundException("Листинг не найден")

        return listing

    async def update_my_listing(self, user_id: UUID, listing_id : UUID, data : ListingUpdateSchemas):

        await self.__check_if_own_listing(user_id=user_id, listing_id=listing_id)
        listing = await self.listing_repo.update(listing_id, data.model_dump(exclude_none=True))

        await self.session.commit()
        await self.session.refresh(listing)

        return listing

    async def close_listing(self, user_id : UUID, listing_id : UUID):
        await self.__check_if_own_listing(user_id=user_id, listing_id=listing_id)
        listing = await self.listing_repo.get_by_id(listing_id)
        validate_transition(LISTING_TRANSITION, listing.status, ListingStatus.CLOSED)
        listing = await self.listing_repo.update(listing_id, status = ListingStatus.CLOSED)

        await self.session.commit()
        await self.session.refresh(listing)

        return listing
