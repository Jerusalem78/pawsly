from src.repositories.base import BaseRepository
from src.models.user import UserOrm
from sqlalchemy import select

class UserRepository(BaseRepository[UserOrm]):

    def __init__(self, session):
        super().__init__(session, UserOrm)

    async def get_by_email(self, email : str) -> UserOrm | None:
        result = await self.session.execute(
            select(UserOrm).where(UserOrm.email==email)
        )

        return result.scalar_one_or_none()