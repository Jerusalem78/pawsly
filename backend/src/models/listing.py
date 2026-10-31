import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from sqlalchemy import CheckConstraint
from uuid import UUID
from src.core.enums import ListingStatus

class ListingOrm(Base):

    __tablename__ = "listings"
    __table_args__ = (
        CheckConstraint("date_start < date_end", name="valid_term"),
        CheckConstraint("price_per_day > 0", name="price_non_negative"),

    )

    id : Mapped[uuidpk]
    date_start : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    date_end : Mapped[datetime.datetime]
    price_per_day : Mapped[int]
    description : Mapped[str | None] = mapped_column(String(2048))
    status : Mapped[ListingStatus] = mapped_column(default=ListingStatus.OPEN)
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    owner_id : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    pet_id : Mapped[UUID] = mapped_column(ForeignKey("pets.id", ondelete="CASCADE"))

    pet : Mapped["PetsOrm"] = relationship(back_populates="listing") # noqa
    owner : Mapped["UserOrm"] = relationship(back_populates="listing") # noqa
    application : Mapped["ApplicationOrm"] = relationship(back_populates="listing") # noqa
    booking : Mapped["BookingOrm"] = relationship(back_populates="listing") # noqa