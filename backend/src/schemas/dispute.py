from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from src.core.enums import DisputeStatus, BookingStatus
from src.schemas.booking import BookingShortGetSchema
from src.schemas.user import UserGetPublicSchema
from datetime import datetime


class DisputePostSchema(BaseModel):
    booking_id: UUID
    reason: str


class DisputeResolveSchema(BaseModel):
    resolution: str
    status: DisputeStatus
    booking_status: BookingStatus
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        allowed = (DisputeStatus.RESOLVED_OWNER, DisputeStatus.RESOLVED_SITTER, DisputeStatus.RESOLVED_SPLIT)
        if v not in allowed:
            raise ValueError("недопустимый статус разрешения")
        return v


class DisputeGetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    booking: BookingShortGetSchema
    opened_by: UserGetPublicSchema
    reason: str
    status: DisputeStatus
    resolution: str | None
    resolved_by: UserGetPublicSchema | None
    created_at: datetime
    resolved_at: datetime | None