import datetime
from sqlalchemy import ForeignKey, func
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from src.core.enums import BookingStatus

class BookingOrm(Base):

    __tablename__="bookings"

    id : Mapped[uuidpk]
    total_amount : Mapped[int]
    status : Mapped[BookingStatus] = mapped_column(default=BookingStatus.PENDING_PAYMENT)
    sitter_done_at : Mapped[datetime.datetime | None]
    owner_confirned_at : Mapped[datetime.datetime | None]
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    listing_id : Mapped[UUID] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"))
    owner_id : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    sitter_id : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    listing : Mapped["ListingOrm"] = relationship(back_populates="booking") # noqa
    owner: Mapped["UserOrm"] = relationship(foreign_keys=[owner_id], back_populates="owner_bookings") # noqa
    sitter: Mapped["UserOrm"] = relationship(foreign_keys=[sitter_id], back_populates="sitter_bookings") # noqa
    dispute: Mapped["DisputeOrm"] = relationship(back_populates="booking") # noqa