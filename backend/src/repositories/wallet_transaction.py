from src.repositories.base import BaseRepository
from src.models.wallet_transaction import WalletTransactionOrm
from sqlalchemy import select
from uuid import UUID


class WalletTransactionRepository(BaseRepository[WalletTransactionOrm]):

    def __init__(self, session):
        super().__init__(session, WalletTransactionOrm)

    async def get_by_wallet_id(self, wallet_id: UUID, offset: int = 0, limit: int = 20) -> list[WalletTransactionOrm]:
        result = await self.session.execute(
            select(WalletTransactionOrm)
            .where(WalletTransactionOrm.wallet_id == wallet_id)
            .order_by(WalletTransactionOrm.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())