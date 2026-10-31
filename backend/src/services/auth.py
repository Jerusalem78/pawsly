from src.repositories.user import UserRepository
from src.repositories.wallet import WalletRepository
from src.core.security import hash_password, verify_password, create_access_token, decode_access_token, create_refresh_token
from src.core.exceptions import ConflictException, UnauthorizedException, NotFoundException
import jwt
from src.schemas.auth import RegisterPostSchema, LoginPostSchema, TokenResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.wallet_repo = WalletRepository(session)

    async def register(self, data: RegisterPostSchema) -> TokenResponseSchema:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ConflictException("Email уже занят")
        

        hashed = hash_password(data.password)
        user = await self.user_repo.create(
            username=data.username,
            email=data.email,
            hashed_password=hashed,
        )

        await self.wallet_repo.create(user_id=user.id)
        await self.session.commit()

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)

    async def login(self, data: LoginPostSchema) -> TokenResponseSchema:
        user = await self.user_repo.get_by_email(data.email)
        if not user:
            raise UnauthorizedException("Неверный email или пароль")

        if not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Неверный email или пароль")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)

    async def get_current_user(self, token: str):
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException()

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Пользователь не найден")

        return user

    async def refresh(self, refresh_token: str) -> TokenResponseSchema:
        try:
            payload = decode_access_token(refresh_token)
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Невалидный refresh токен")
        
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Неверный тип токена")
        
        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Пользователь не найден")
        
        access_token = create_access_token({"sub": str(user.id)})
        new_refresh = create_refresh_token({"sub": str(user.id)})
        return TokenResponseSchema(access_token=access_token, refresh_token=new_refresh)

    
    