from pydantic import BaseModel, Field, model_validator, ConfigDict, field_validator
from uuid import UUID
from src.core.enums import ListingStatus, Spicies
from datetime import datetime, timezone
from src.schemas.pet import PetShortGetSchema

class ListingPostSchema(BaseModel):

    pet_id : UUID
    date_start : datetime
    date_end : datetime
    price_per_day : int = Field(gt=0)
    description : str | None = Field(default=None, max_length=2048)

    @field_validator("date_start", "date_end", mode="before")
    @classmethod
    def normalize_datetime(cls, value):
        if value is None:
            return value

        dt = value if isinstance(value, datetime) else datetime.fromisoformat(value)

        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)

        return dt

    @model_validator(mode="after")
    def validate_dates(self):
        if self.date_start >= self.date_end:
            raise ValueError("date_end must be later than date_start")
        return self

class ListingGetSchema(BaseModel):
    id: UUID
    owner_id: UUID
    pet: PetShortGetSchema
    date_start: datetime
    date_end: datetime
    price_per_day: int
    description: str | None
    status: ListingStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ListingUpdateSchemas(BaseModel):

    date_start : datetime | None = None
    date_end : datetime | None = None
    price_per_day : int | None = Field(default=None, gt=0)
    description : str | None = Field(default=None, max_length=2048)

class ListingFilterSchema(BaseModel):

    date_start : datetime | None = None
    date_end : datetime | None = None
    spicies : Spicies | None = None
    min_price : int | None = Field(default=None, gt=0)
    max_price : int | None = Field(default=None, gt=0)     


    @model_validator(mode="after")
    def validate_prices_and_dates(self):
        if  self.min_price and self.max_price and self.min_price > self.max_price:
            raise ValueError("min price gt than max price")
        if self.date_start and self.date_end and self.date_start > self.date_end :
            raise ValueError("start date gt than date end")
        return self
    




