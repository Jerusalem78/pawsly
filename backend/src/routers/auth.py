from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.services.auth import AuthService
from src.schemas.auth import RegisterPostSchema, LoginPostSchema, TokenResponseSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=TokenResponseSchema)
async def register(
    data: RegisterPostSchema,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)
    return await service.register(data)


@auth_router.post("/login", response_model=TokenResponseSchema)
async def login(
    data: LoginPostSchema,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)
    return await service.login(data)