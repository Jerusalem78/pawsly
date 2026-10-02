from src.repositories.wallet import WalletRepository
from src.repositories.wallet_transaction import WalletTransactionRepository
from src.core.exceptions import NotFoundException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.core.enums import TransactionType

class EscrowService:
    def __init__(self, session: AsyncSession):
        self.session : AsyncSession = session
        self.wallet_repo = WalletRepository(session)
        self.transaction_repo = WalletTransactionRepository(session)

    async def hold(self, user_id: UUID, amount : int):
        wallet = await self.wallet_repo.get_by_user_id(user_id)

        if not wallet:
            raise NotFoundException("кошелек не найден")

        if wallet.balance < amount:
            raise BadRequestException("Не достаточно средств")

        wallet = await self.wallet_repo.transfer_to_escrow(wallet.id, amount)

        transaction = await self.transaction_repo.create(
            wallet_id=wallet.id,
            amount=amount,
            type=TransactionType.ESCROW_HOLD,
        )

        await self.session.commit()
        await self.session.refresh(wallet)
        await self.session.refresh(transaction)

        return wallet

    async def payout(self, booking):
        owner_wallet = await self.wallet_repo.get_by_user_id(booking.owner_id)
        sitter_wallet = await self.wallet_repo.get_by_user_id(booking.sitter_id)
        if owner_wallet.escrow_balance < booking.total_amount:
            raise BadRequestException("Недостаточно средств в эскроу")
        
        await self.wallet_repo.transfer_from_escrow(owner_wallet.id, booking.total_amount)
        await self.wallet_repo.add_balance(sitter_wallet.id, booking.total_amount)
        
        await self.transaction_repo.create(
            wallet_id=owner_wallet.id,
            amount=booking.total_amount,
            type=TransactionType.ESCROW_RELEASE,
        )
        await self.transaction_repo.create(
            wallet_id=sitter_wallet.id,
            amount=booking.total_amount,
            type=TransactionType.PAYOUT,
        )
        
        await self.session.commit()

    async def refund(self, booking):
        owner_wallet = await self.wallet_repo.get_by_user_id(booking.owner_id)

        if not owner_wallet:
            raise NotFoundException("Кошелёк не найден")

        if owner_wallet.escrow_balance < booking.total_amount:
            raise BadRequestException("Недостаточно средств в эскроу")

        await self.wallet_repo.transfer_from_escrow(owner_wallet.id, booking.total_amount)

        await self.transaction_repo.create(
            wallet_id=owner_wallet.id,
            amount=booking.total_amount,
            type=TransactionType.REFUND,
        )

        await self.session.commit()


    async def split(self, booking):
        owner_wallet = await self.wallet_repo.get_by_user_id(booking.owner_id)
        sitter_wallet = await self.wallet_repo.get_by_user_id(booking.sitter_id)

        if not owner_wallet or not sitter_wallet:
            raise NotFoundException("Кошелёк не найден")

        if owner_wallet.escrow_balance < booking.total_amount:
            raise BadRequestException("Недостаточно средств в эскроу")

        half = booking.total_amount // 2

        await self.wallet_repo.transfer_from_escrow(owner_wallet.id, booking.total_amount)
        await self.wallet_repo.add_balance(owner_wallet.id, half)
        await self.wallet_repo.add_balance(sitter_wallet.id, half)

        await self.transaction_repo.create(
            wallet_id=owner_wallet.id,
            amount=half,
            type=TransactionType.SPLIT_REFUND,
        )
        await self.transaction_repo.create(
            wallet_id=sitter_wallet.id,
            amount=half,
            type=TransactionType.SPLIT_PAYOUT,
        )

        await self.session.commit()
        
        