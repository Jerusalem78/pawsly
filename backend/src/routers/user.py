from fastapi import APIRouter, Depends
from src.services.user import UserService
from src.services.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.schemas.user import UserGetPrivateSchema, UserGetPublicSchema, UserUpdateSchema
from uuid import UUID

user_router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


@user_router.get("/me", response_model=UserGetPrivateSchema)
async def get_me(
    user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserGetPrivateSchema:
    return await service.get_me(user_id=user.id)


@user_router.patch("/me", response_model=UserGetPrivateSchema)
async def update_me(
    data: UserUpdateSchema,
    user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserGetPrivateSchema:
    return await service.update_me(user_id=user.id, data=data)


@user_router.get("/{user_id}", response_model=UserGetPublicSchema)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserGetPublicSchema:
    return await service.get_user(user_id=user_id)