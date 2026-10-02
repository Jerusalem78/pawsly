from src.repositories.user import UserRepository
from src.core.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserUpdateSchema
from uuid import UUID

class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def get_me(self, user_id: UUID):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Пользователь не найден")
        return user

    async def update_me(self, user_id: UUID, data: UserUpdateSchema):
        user = await self.user_repo.update(user_id, **data.model_dump(exclude_none=True))
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user(self, user_id: UUID):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Пользователь не найден")
        return user