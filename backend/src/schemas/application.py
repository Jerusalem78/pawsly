from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID
from src.core.enums import ApplicationStatus
from src.schemas.user import UserGetPublicSchema
from src.schemas.listing import ListingGetSchema
from datetime import datetime

class ApplicationPostSchema(BaseModel):
    listing_id : UUID
    message : str | None = Field(default=None, max_length=2048)

class ApplicationGetSchema(BaseModel):
    id : UUID
    listing : ListingGetSchema
    sitter : UserGetPublicSchema
    message : str | None
    status : ApplicationStatus
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdateSchema(BaseModel):
    status : ApplicationStatus

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in (ApplicationStatus.ACCEPTED, ApplicationStatus.REJECTED):
            raise ValueError("ALLOWED ONLY ACCEPTED OR REJECTED")
        return v
    