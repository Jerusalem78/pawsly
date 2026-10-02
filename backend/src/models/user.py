import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from src.core.enums import Role


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(default=Role.OWNER)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )

    wallet: Mapped["WalletOrm"] = relationship(back_populates="user")  # noqa
    pets: Mapped[list["PetsOrm"]] = relationship(back_populates="owner")  # noqa
    listing: Mapped[list["ListingOrm"]] = relationship(back_populates="owner")  # noqa
    application: Mapped[list["ApplicationOrm"]] = relationship(back_populates="sitter")  # noqa
    owner_bookings: Mapped[list["BookingOrm"]] = relationship(foreign_keys="BookingOrm.owner_id", back_populates="owner")  # noqa
    sitter_bookings: Mapped[list["BookingOrm"]] = relationship(foreign_keys="BookingOrm.sitter_id", back_populates="sitter")  # noqa
    disputes_opened: Mapped[list["DisputeOrm"]] = relationship(foreign_keys="DisputeOrm.opened_by", back_populates="user")  # noqa
    disputes_resolved: Mapped[list["DisputeOrm"]] = relationship(foreign_keys="DisputeOrm.resolved_by", back_populates="admin")  # noqa