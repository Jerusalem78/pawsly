import datetime
from sqlalchemy import ForeignKey, String, func
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from src.core.enums import Spicies
from sqlalchemy import CheckConstraint


class PetsOrm(Base):
    __tablename__ =  "pets"
    __table_args__=(
        CheckConstraint("age > 0", name="age_non_negative"),
    )

    id : Mapped[uuidpk]
    owner_id : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name : Mapped[str] = mapped_column(String(100))
    spices : Mapped[Spicies]
    breed : Mapped[str | None] = mapped_column(String(100))
    age : Mapped[int]
    special_notes : Mapped[str | None] = mapped_column(String(2048))
    is_active : Mapped[bool] = mapped_column(default=True)
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    owner : Mapped["UserOrm"] = relationship(back_populates="pets") # noqa
    listing : Mapped["ListingOrm"] = relationship(back_populates="pets") # noqa