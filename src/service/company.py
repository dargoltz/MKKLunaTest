import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload

from .industry import IndustryService
from .building import BuildingService
from ..core import database_manager
from ..dto import CompanyPostRequest, CompanyPutRequest
from ..models import Company, Industry, company_industry


class CompanyService:
    def __init__(self, session: AsyncSession = Depends(database_manager.get_db)):
        self.session = session
        self.building_service = BuildingService(session)
        self.industry_service = IndustryService(session)

    async def create_item(self, request: CompanyPostRequest) -> Company:
        item = Company(
            name=request.name,
            phone_numbers=request.phone_numbers,
            building_id=request.building_id
        )

        self.session.add(item)
        await self.session.flush()

        for industry_id in request.industry_ids:
            await self.session.execute(
                insert(company_industry).values(
                    company_id=item.id,
                    industry_id=industry_id
                )
            )

        return await self.get_item(item.id)

    async def update_item(self, item_id: uuid.UUID, request: CompanyPutRequest) -> Company:
        item = await self.get_item(item_id)

        for key, value in request.model_dump(mode="json", exclude_unset=True).items():
            setattr(item, key, value)

        if request.industry_ids is not None:
            for industry_id in request.industry_ids:
                await self.session.execute(
                    delete(company_industry).where(
                        company_industry.c.company_id == item.id,
                    )
                )

                await self.session.execute(
                    insert(company_industry).values(
                        company_id=item.id,
                        industry_id=industry_id
                    )
                )

        await self.session.flush()
        await self.session.refresh(item)

        return item

    async def get_item(self, item_id: uuid.UUID) -> Company:
        query = await self.session.execute(
            select(Company).where(Company.id == item_id)
            .options(selectinload(Company.industries))
            .options(selectinload(Company.building))
        )

        item = query.scalars().one_or_none()

        if not item:
            raise HTTPException(status_code=404)

        return item

    async def delete_item(self, item_id: uuid.UUID):
        item = await self.get_item(item_id)

        await self.session.delete(item)

    async def get_by_building(self, building_id: uuid.UUID) -> list[Company]:
        query = await self.session.execute(
            select(Company).where(Company.building_id == building_id)
        )

        items = query.scalars().all()

        return list(items)

    async def get_by_industry(self, industry_id: uuid.UUID, strict: bool = False) -> list[Company]:
        if strict:
            query = await self.session.execute(
                select(Company).join(Company.industries).where(Industry.id == industry_id)
            )

            items = query.scalars().unique().all()

            return list(items)
        else:
            industry_children = await self.industry_service.get_industry_children(industry_id)

            industry_ids = [industry.id for industry in industry_children] + [industry_id]

            query = await self.session.execute(
                select(Company).join(Company.industries).where(Industry.id.in_(industry_ids))
            )

            items = query.scalars().unique().all()

            return list(items)

    async def get_by_name(self, name: str) -> Company:
        if len(name) < 3:
            raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")

        query = await self.session.execute(
            select(Company).where(Company.name == name).options(selectinload(Company.industries))
        )

        item = query.scalars().one_or_none()

        if not item:
            raise HTTPException(status_code=404)

        return item

    async def get_by_coordinate(
        self,
        latitude: float,
        longitude: float,
        radius: int
    ) -> list[Company]:
        if radius < 0:
            raise HTTPException(status_code=400, detail="Radius must be positive")

        if not -90 < latitude < 90:
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")

        if not -90 < longitude < 90:
            raise HTTPException(status_code=400, detail="Longitude must be between -90 and 90")

        buildings = await self.building_service.get_in_radius(latitude, longitude, radius)

        company_ids = [company.id for building in buildings for company in building.companies]

        query = await self.session.execute(
            select(Company).where(Company.id.in_(company_ids))
        )

        companies = query.scalars().all()

        return list(companies)
