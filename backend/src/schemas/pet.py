from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from src.core.enums import Spicies
from datetime import datetime


class PetShortGetSchema(BaseModel):
    id : UUID
    name : str = Field(max_length=100)
    spicies : Spicies
    age : int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)

class PetGetSchema(PetShortGetSchema):
    owner_id : UUID
    breed : str | None 
    special_notes : str | None
    is_active : bool
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class PetPostSchema(BaseModel):
    name : str = Field(max_length=100)
    spicies : Spicies
    breed : str | None = Field(default=None, max_length=100)
    age : int
    special_notes : str | None

class PetUpdateSchema(BaseModel):
    name : str | None = Field(default=None, max_length=100)
    breed : str | None = Field(default=None, max_length=100)
    age : int | None = Field(default=None, ge=0)
    special_notes : str | None = None