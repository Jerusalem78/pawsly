from src.repositories.booking import BookingRepository
from src.core.exceptions import NotFoundException, ForbiddenException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.services.escrow import EscrowService
from src.core.enums import BookingStatus
from src.core.state_machine import BOOKING_TRANSITIONS, validate_transition

class BookingService:


    def __init__(self, session):
        self.session : AsyncSession = session
        self.booking_repo = BookingRepository(session)
        self.escrow_service = EscrowService(session)
        


    async def sitter_done(self, sitter_id: UUID, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise NotFoundException("Букинг не найден")
        if booking.sitter_id != sitter_id:
            raise ForbiddenException("Это не ваш букинг")
        validate_transition(BOOKING_TRANSITIONS, booking.status, BookingStatus.SITTER_DONE)
        booking = await self.booking_repo.update(
            id = booking.id,
            status = BookingStatus.SITTER_DONE
        )

        await self.session.commit()
        await self.session.refresh(booking)

        return booking

    async def confirm(self, owner_id: UUID, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)

        if not booking:
           raise NotFoundException("Букинг не найден")
    
        if booking.owner_id != owner_id:
            raise ForbiddenException("Не ваш букинг")
    
        validate_transition(BOOKING_TRANSITIONS, booking.status, BookingStatus.COMPLETED)
    
        await self.booking_repo.update(booking_id, status=BookingStatus.COMPLETED)
        await self.escrow_service.payout(booking)

        await self.session.commit()
        return booking


    async def cancel(self, user_id: UUID, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)
        
        if not booking:
            raise NotFoundException("Букинг не найден")
        
        if booking.owner_id != user_id and booking.sitter_id != user_id:
            raise ForbiddenException("Не ваш букинг")
        
        validate_transition(BOOKING_TRANSITIONS, booking.status, BookingStatus.CANCELLED)
        
        await self.booking_repo.update(booking_id, status=BookingStatus.CANCELLED)
        await self.escrow_service.refund(booking)
        
        await self.session.commit()
        return booking

    async def get_my_bookings(self, user_id: UUID, offset: int = 0, limit: int = 20):
        bookings = await self.booking_repo.get_by_owner_id(user_id, offset=offset, limit=limit)
        return bookings

    async def get_booking(self, booking_id: UUID, user_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise NotFoundException("Букинг не найден")
        if booking.owner_id != user_id and booking.sitter_id != user_id:
            raise ForbiddenException("Не ваш букинг")
        return booking