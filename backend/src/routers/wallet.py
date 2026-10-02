from fastapi import APIRouter, Depends
from src.services.wallet import WalletService
from src.services.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.schemas.wallet import WalletReadSchema, DepositRequestSchema, TransactionReadSchema
from typing import List

wallet_router = APIRouter(prefix="/wallet", tags=["wallet"])


def get_wallet_service(session: AsyncSession = Depends(get_db)) -> WalletService:
    return WalletService(session)


@wallet_router.get("/", response_model=WalletReadSchema)
async def get_wallet(
    user=Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
) -> WalletReadSchema:
    return await service.get_wallet(user_id=user.id)


@wallet_router.post("/deposit", response_model=WalletReadSchema)
async def deposit(
    data: DepositRequestSchema,
    user=Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
) -> WalletReadSchema:
    return await service.deposit(user_id=user.id, amount=data.amount)


@wallet_router.get("/transactions", response_model=List[TransactionReadSchema])
async def get_transactions(
    offset: int = 0,
    limit: int = 20,
    user=Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
) -> List[TransactionReadSchema]:
    return await service.get_transaction(user_id=user.id)