from sqlalchemy import ForeignKey
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from sqlalchemy import CheckConstraint

class WalletOrm(Base):

    __tablename__ = "wallets"

    __table_args__ = (
        CheckConstraint("balance >= 0", name="balance_non_negative"),
        CheckConstraint("escrow_balance >= 0", name="escrow_balance_non_negative"),
    )

    id : Mapped[uuidpk]
    balance : Mapped[int] = mapped_column(default=0)
    escrow_balance : Mapped[int] = mapped_column(default=0)
    user_id : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    user : Mapped["UserOrm"] = relationship(back_populates="wallet") # noqa
    wallet_transaction: Mapped[list["WalletTransactionOrm"]] = relationship(back_populates="wallet")  # noqa # noqa
