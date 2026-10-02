import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from src.core.enums import DisputeStatus
from uuid import UUID

class DisputeOrm(Base):

    __tablename__ = "disputes"

    id : Mapped[uuidpk]
    reason : Mapped[str] = mapped_column(String(4096))
    status : Mapped[DisputeStatus] = mapped_column(default=DisputeStatus.OPEN)
    resolution : Mapped[str | None] = mapped_column(String(2048))
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    resolved_at : Mapped[datetime.datetime | None]
    opened_by : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    resolved_by : Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    booking_id: Mapped[UUID] = mapped_column(ForeignKey("bookings.id", ondelete="RESTRICT"), unique=True)

    user: Mapped["UserOrm"] = relationship(foreign_keys=[opened_by], back_populates="disputes_opened") # noqa
    admin: Mapped["UserOrm"] = relationship(foreign_keys=[resolved_by], back_populates="disputes_resolved") # noqa
    booking: Mapped["BookingOrm"] = relationship(back_populates="dispute") # noqa
    



