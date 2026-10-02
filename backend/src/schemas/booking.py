from pydantic import BaseModel, ConfigDict
from uuid import UUID
from src.core.enums import BookingStatus
from src.schemas.listing import ListingGetSchema
from src.schemas.user import UserGetPublicSchema
from datetime import datetime

class BookingShortGetSchema(BaseModel):

    id: UUID
    status: BookingStatus
    total_amount: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BookingGetSchema(BookingShortGetSchema):
    listing: ListingGetSchema
    owner: UserGetPublicSchema
    sitter: UserGetPublicSchema
    sitter_done_at: datetime | None
    owner_confirmed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
    
