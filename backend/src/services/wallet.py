from src.repositories.wallet import WalletRepository
from src.repositories.wallet_transaction import WalletTransactionRepository
from src.core.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

class WalletService:

    def __init__(self, session : AsyncSession):
        self.session : AsyncSession = session
        self.wallet_repo = WalletRepository(session)
        self.wallet_transaction_repo = WalletTransactionRepository(session)


    async def get_wallet(self, user_id : UUID):
        wallet = await self.wallet_repo.get_by_user_id(user_id)
        if not wallet:
            raise NotFoundException("Кошелек не найден")

        wallet.balance = wallet.balance / 100
        return wallet

    async def deposit(self, user_id: UUID, amount : int):
        wallet = self.get_wallet(user_id)
        wallet = await self.wallet_repo.add_balance(
            wallet_id=wallet.id, amount=amount
        )

        await self.session.commit()
        await self.session.refresh(wallet)

        return wallet

    async def get_transaction(self, user_id : UUID):
        wallet_id = await self.get_wallet(user_id)
        transaction = await self.wallet_transaction_repo.get_by_wallet_id(wallet_id.id) 
        return transaction