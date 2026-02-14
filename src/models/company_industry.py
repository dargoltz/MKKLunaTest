from sqlalchemy import Table, Column, UUID, ForeignKey

from .base import Base

company_industry = Table(
    "company_industry",
    Base.metadata,
    Column("company_id", UUID(as_uuid=True), ForeignKey("companies.id"), primary_key=True),
    Column("industry_id", UUID(as_uuid=True), ForeignKey("industries.id"), primary_key=True),
)