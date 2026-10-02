import datetime
from sqlalchemy import ForeignKey, String, func
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.database import Base, uuidpk
from src.core.enums import ApplicationStatus

class ApplicationOrm(Base):

    __tablename__ = "applications"
    
    id : Mapped[uuidpk]
    messege : Mapped[str | None] = mapped_column(String(2048))
    status : Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.PENDING)
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    listing_id : Mapped[UUID] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"))
    sitter_id : Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    listing : Mapped["ListingOrm"] = relationship(back_populates="application") # noqa
    sitter : Mapped["UserOrm"] = relationship(back_populates="application") # noqa