from src.repositories.base import BaseRepository
from src.models.wallet import WalletOrm
from sqlalchemy import select, update as UPD
from uuid import UUID


class WalletRepository(BaseRepository[WalletOrm]):

    def __init__(self, session):
        super().__init__(session, WalletOrm)

    async def get_by_user_id(self, user_id: UUID, offset: int = 0, limit: int = 20) -> WalletOrm | None:
        result = await self.session.execute(
            select(WalletOrm).where(WalletOrm.user_id == user_id).offset(offset).limit(limit)
        )
        return result.scalar_one_or_none()

    async def add_balance(self, wallet_id: UUID, amount: int) -> WalletOrm:
        result = await self.session.execute(
            UPD(WalletOrm)
            .where(WalletOrm.id == wallet_id)
            .values(balance=WalletOrm.balance + amount)
            .returning(WalletOrm)
        )
        return result.scalar_one()

    async def decrease_balance(self, wallet_id: UUID, amount: int) -> WalletOrm:
            result = await self.session.execute(
                UPD(WalletOrm)
                .where(WalletOrm.id == wallet_id)
                .values(balance=WalletOrm.balance - amount)
                .returning(WalletOrm)
            )
            return result.scalar_one()

    async def transfer_to_escrow(self, wallet_id: UUID, amount: int) -> WalletOrm:
        result = await self.session.execute(
            UPD(WalletOrm)
            .where(WalletOrm.id == wallet_id)
            .values(
                balance=WalletOrm.balance - amount,
                escrow_balance=WalletOrm.escrow_balance + amount,
            )
            .returning(WalletOrm)
        )
        return result.scalar_one()

    async def transfer_from_escrow(self, wallet_id: UUID, amount: int) -> WalletOrm:
            result = await self.session.execute(
                UPD(WalletOrm)
                .where(WalletOrm.id == wallet_id)
                .values(
                    balance=WalletOrm.balance + amount,
                    escrow_balance=WalletOrm.escrow_balance - amount,
                )
                .returning(WalletOrm)
            )
            return result.scalar_one()