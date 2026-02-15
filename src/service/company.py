import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import database_manager
from ..dto import CompanyPostRequest, CompanyPutRequest
from ..models import Company


class CompanyService:
    def __init__(self, session: AsyncSession = Depends(database_manager.get_db)):
        self.session = session

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

        for key, value in request.model_dump(mode="json").items():
            setattr(item, key, value)

        await self.session.flush()

        return item

    async def get_item(self, item_id: uuid.UUID) -> Company:
        item = await self.session.get(Company, item_id)

        if not item:
            raise HTTPException(status_code=404)

        return item

    async def delete_item(self, item_id: uuid.UUID):
        item = await self.get_item(item_id)

        await self.session.delete(item)
