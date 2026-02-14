import uuid
from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Industry(Base):
    __tablename__ = "industries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("industries.id"), nullable=True)

    parent: Mapped["Industry"] = relationship(
        argument="Industry",
        remote_side=[id],
        back_populates="children",
        lazy="selectin"
    )
    children: Mapped[list["Industry"]] = relationship(
        argument="Industry",
        back_populates="parent",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    companies: Mapped[list["Company"]] = relationship(
        argument="Company",
        secondary="company_industry",
        back_populates="industries",
        lazy="selectin"
    )
