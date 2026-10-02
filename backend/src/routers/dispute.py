from fastapi import APIRouter, Depends
from src.services.dispute import DisputeService
from src.services.deps import get_current_user, require_admin
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.schemas.dispute import DisputePostSchema, DisputeGetSchema, DisputeResolveSchema
from uuid import UUID
from typing import List

dispute_router = APIRouter(prefix="/disputes", tags=["disputes"])


def get_dispute_service(session: AsyncSession = Depends(get_db)) -> DisputeService:
    return DisputeService(session)


@dispute_router.post("/create", response_model=DisputeGetSchema)
async def open_dispute(
    data: DisputePostSchema,
    user=Depends(get_current_user),
    service: DisputeService = Depends(get_dispute_service),
) -> DisputeGetSchema:
    return await service.open_dispute(user_id=user.id, data=data)


@dispute_router.get("/{booking_id}", response_model=DisputeGetSchema)
async def get_dispute(
    booking_id: UUID,
    user=Depends(get_current_user),
    service: DisputeService = Depends(get_dispute_service),
) -> DisputeGetSchema:
    return await service.get_dispute(booking_id=booking_id, user_id=user.id)


@dispute_router.get("/open", response_model=List[DisputeGetSchema])
async def get_open_disputes(
    service: DisputeService = Depends(get_dispute_service),
    user=Depends(require_admin),
) -> List[DisputeGetSchema]:
    return await service.get_open_disputes()


@dispute_router.patch("/resolve/{dispute_id}", response_model=DisputeGetSchema)
async def resolve_dispute(
    dispute_id: UUID,
    data: DisputeResolveSchema,
    user=Depends(require_admin),
    service: DisputeService = Depends(get_dispute_service),
) -> DisputeGetSchema:
    return await service.resolve_dispute(admin_id=user.id, dispute_id=dispute_id, data=data)