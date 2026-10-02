from src.repositories.dispute import DisputeRepository
from src.repositories.user import UserRepository
from src.repositories.booking import BookingRepository
from src.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.schemas.dispute import DisputePostSchema, DisputeResolveSchema
from src.core.enums import BookingStatus, DisputeStatus
from src.services.escrow import EscrowService
from src.core.state_machine import BOOKING_TRANSITIONS, validate_transition

class DisputeService:

    def __init__(self, session : AsyncSession):
        self.session = session
        self.dispute_repo = DisputeRepository(session)
        self.booking_repo = BookingRepository(session)
        self.user_repo = UserRepository(session)
        self.escrow_service = EscrowService(session)

    async def __checkifyours(self, booking, user_id):
        if booking.owner_id != user_id and booking.sitter_id != user_id:
            raise ForbiddenException("Вы не член букинга")
        
    async def open_dispute(self, user_id:UUID, data: DisputePostSchema):
        booking = await self.booking_repo.get_by_id(data.booking_id)
        
        if not booking:
            raise NotFoundException("букинг не найден")
        await self.__checkifyours(booking, user_id)
        if booking.status != BookingStatus.SITTER_DONE:
            raise BadRequestException("Букинг еще не закрыт")
        validate_transition(BOOKING_TRANSITIONS, booking.status, BookingStatus.DISPUTED)
        dispute = await self.dispute_repo.create(
            booking_id = data.booking_id,
            reason = data.reason,
            opened_by = user_id,
        )
        booking = await self.booking_repo.update(data.booking_id, status = BookingStatus.DISPUTED)

        await self.session.commit()
        await self.session.refresh(dispute)
        await self.session.refresh(booking)

        return dispute


    async def get_dispute(self, booking_id):

        dispute = await self.dispute_repo.get_by_booking_id(booking_id)

        return dispute

    async def get_open_dispute(self):
    
        dispute = await self.dispute_repo.get_open_disputes()
        return dispute

async def resolve_dispute(self, admin_id: UUID, dispute_id: UUID, data: DisputeResolveSchema):
        dispute = await self.dispute_repo.get_by_id(dispute_id)
        if not dispute:
            raise NotFoundException("Спор не найден")

        booking = await self.booking_repo.get_by_id(dispute.booking_id)
        if not booking:
            raise NotFoundException("Букинг не найден")

        validate_transition(BOOKING_TRANSITIONS, booking.status, data.booking_status)

        await self.dispute_repo.update(dispute_id,
            status=DisputeStatus.RESOLVED,
            resolution=data.resolution,
            resolved_by=admin_id,
        )

        await self.booking_repo.update(dispute.booking_id, status=data.booking_status)

        if data.booking_status == BookingStatus.RESOLVED_OWNER:
            await self.escrow_service.refund(booking)
        elif data.booking_status == BookingStatus.RESOLVED_SITTER:
            await self.escrow_service.payout(booking)
        elif data.booking_status == BookingStatus.RESOLVED_SPLIT:
            await self.escrow_service.split(booking)

        await self.session.commit()
        return dispute

        




        
