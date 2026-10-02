import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from uuid import UUID
from src.core.enums import TransactionType
from sqlalchemy import CheckConstraint


class WalletTransactionOrm(Base):
    __tablename__ = 'wallet_transaction'
    __table_args__ = (
        CheckConstraint("amount > 0", name="amount_non_negative"),
    )

    id : Mapped[uuidpk]
    wallet_id : Mapped[UUID] = mapped_column(ForeignKey('wallets.id'))
    amount : Mapped[int] 
    TypeTransaction : Mapped[TransactionType] 
    ref_id : Mapped[UUID] = mapped_column(ForeignKey("bookings.id"))
    created_at : Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )

    wallet: Mapped["WalletOrm"] = relationship(back_populates="wallet_transaction")  # noqa # noqa