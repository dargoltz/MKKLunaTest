import uuid
from sqlalchemy import ARRAY, String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .industry import Industry
from .building import Building


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_numbers: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    building_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("buildings.id", ondelete="RESTRICT"), nullable=True)

    building: Mapped["Building"] = relationship(
        argument="Building",
        back_populates="companies",
        lazy="selectin"
    )
    industries: Mapped[list["Industry"]] = relationship(
        argument="Industry",
        secondary="company_industry",
        back_populates="companies",
        lazy="selectin"
    )
