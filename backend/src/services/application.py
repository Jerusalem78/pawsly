from src.repositories.listing import ListingRepository
from src.repositories.booking import BaseRepository
from src.repositories.application import ApplicationRepository
from src.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.application import ApplicationPostSchema
from uuid import UUID
from src.core.enums import ListingStatus
from src.core.enums import ApplicationStatus
from src.core.state_machine import APPLICATION_TRANSITION, validate_transition

class ApplicationService:
    def __init__(self, session):
        self.session : AsyncSession = session
        self.application_repo = ApplicationRepository(session)
        self.listing_repo = ListingRepository(session)
        self.booking_repo = BaseRepository(session)

    async def get_my_application(self, user_id: UUID, limit : int = 20, offset : int = 0):
        application = await self.application_repo.get_by_sitter_id(user_id, limit, offset)

        return application

    async def get_listing_application(self, listing_id, user_id):
        listing = await self.listing_repo.get_by_id(listing_id)

        if listing.owner_id != user_id:
            raise ForbiddenException("вы не владелец")

        application = await self.application_repo.get_by_listing_id(listing_id=listing_id)

        return application

    async def create_application(self, data : ApplicationPostSchema):

        listing = await self.listing_repo.get_by_listing_id(
            data.listing_id
        ) 
        if listing.status != ListingStatus.OPEN:
            BadRequestException("ваша заявка не открыта")

        application = await self.application_repo.create(
            listing_id = data.listing_id,
            message = data.message
        )

        await self.session.execute()
        await self.session.refresh(application)

        return application

    async def accept_application(self, user_id: UUID, application_id: UUID):
        application = await self.application_repo.get_by_id(application_id)
        
        if not application:
            raise NotFoundException("Заявка не найдена")
        
        listing = await self.listing_repo.get_by_id(application.listing_id)
        
        if listing.owner_id != user_id:
            raise ForbiddenException("Не ваш листинг")
        
        validate_transition(APPLICATION_TRANSITION, application.status, ApplicationStatus.ACCEPTED)
        
        await self.application_repo.update(application_id, status=ApplicationStatus.ACCEPTED)
        await self.application_repo.reject_all_except(listing.id, application_id)
        
        await self.listing_repo.update(listing.id, status=ListingStatus.MATCHED)
        
        booking = await self.booking_repoww.create(
            listing_id=listing.id,
            owner_id=user_id,
            sitter_id=application.sitter_id,
            total_amount=listing.price_per_day * (listing.date_end - listing.date_start).days,
        )
        
        await self.session.commit()
        return booking
            
            
