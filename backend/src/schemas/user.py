from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from src.core.enums import Role
from datetime import datetime


class UserGetPublicSchema(BaseModel):
    username : str = Field(min_length=3, max_length=50)
    role : Role

    model_config = ConfigDict(from_attributes=True)

class UserGetPrivateSchema(UserGetPublicSchema):
    id : UUID
    email : EmailStr
    is_active : bool
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchema(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None

