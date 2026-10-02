from pydantic import BaseModel, EmailStr, Field
from src.core.enums import Role
class LoginPostSchema(BaseModel):
    email : EmailStr
    password : str = Field(min_length=8)

class RegisterPostSchema(LoginPostSchema):
    username : str
    role : Role

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None