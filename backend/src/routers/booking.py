from fastapi import APIRouter, Depends
from src.services.booking import BookingService
from src.services.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.schemas.booking import BookingGetSchema, BookingShortGetSchema
from uuid import UUID
from typing import List

booking_router = APIRouter(prefix="/bookings", tags=["bookings"])


def get_booking_service(session: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(session)


@booking_router.get("/my", response_model=List[BookingShortGetSchema])
async def get_my_bookings(
    offset: int = 0,
    limit: int = 20,
    service: BookingService = Depends(get_booking_service),
    user=Depends(get_current_user),
) -> List[BookingShortGetSchema]:
    return await service.get_my_bookings(user_id=user.id, offset=offset, limit=limit)


@booking_router.get("/{booking_id}", response_model=BookingGetSchema)
async def get_booking(
    booking_id: UUID,
    service: BookingService = Depends(get_booking_service),
    user=Depends(get_current_user),
) -> BookingGetSchema:
    return await service.get_booking(booking_id=booking_id, user_id=user.id)


@booking_router.patch("/{booking_id}/sitter-done", response_model=BookingGetSchema)
async def sitter_done(
    booking_id: UUID,
    service: BookingService = Depends(get_booking_service),
    user=Depends(get_current_user),
) -> BookingGetSchema:
    return await service.sitter_done(sitter_id=user.id, booking_id=booking_id)


@booking_router.patch("/{booking_id}/confirm", response_model=BookingGetSchema)
async def confirm_booking(
    booking_id: UUID,
    service: BookingService = Depends(get_booking_service),
    user=Depends(get_current_user),
) -> BookingGetSchema:
    return await service.confirm(owner_id=user.id, booking_id=booking_id)


@booking_router.patch("/{booking_id}/cancel", response_model=BookingGetSchema)
async def cancel_booking(
    booking_id: UUID,
    service: BookingService = Depends(get_booking_service),
    user=Depends(get_current_user),
) -> BookingGetSchema:
    return await service.cancel(user_id=user.id, booking_id=booking_id)