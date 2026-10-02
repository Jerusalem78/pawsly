from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.security import decode_access_token
from src.core.exceptions import UnauthorizedException, NotFoundException
from src.core.enums import Role
from src.core.exceptions import ForbiddenException
from src.repositories.user import UserRepository
from src.models.user import UserOrm
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> UserOrm:
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Токен истёк")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Невалидный токен")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise NotFoundException("Пользователь не найден")

    return user


async def require_admin(user: UserOrm = Depends(get_current_user)) -> UserOrm:
    if user.role != Role.ADMIN:
        raise ForbiddenException()
    return user