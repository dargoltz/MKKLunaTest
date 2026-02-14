import uuid
from sqlalchemy import String, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)


    companies: Mapped[list["Company"]] = relationship(
        argument="Company",
        back_populates="building",
        lazy="selectin",
    )
