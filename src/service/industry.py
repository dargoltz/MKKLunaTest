import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..core import database_manager
from ..dto import IndustryPostRequest, IndustryPutRequest
from ..models import Industry


class IndustryService:
    def __init__(self, session: AsyncSession = Depends(database_manager.get_db)):
        self.session = session

    async def create_item(self, request: IndustryPostRequest) -> Industry:
        """Здесь можно написать рекурсивный запрос для проверки, но я пообещал эйчару сделать приложение за 5ч и уже не успеваю"""
        if request.parent_id:
            parent = await self.get_item(request.parent_id)

            if parent.parent_id:
                grandparent = await self.get_item(parent.parent_id)

                if grandparent.parent_id:
                    raise HTTPException(status_code=400, detail="Industry hierarchy depth is limited to 3")

        item = Industry(
            name=request.name,
            parent_id=request.parent_id
        )

        self.session.add(item)
        await self.session.flush()

        return item

    async def update_item(self, item_id: uuid.UUID, request: IndustryPutRequest) -> Industry:
        item = await self.get_item(item_id)

        for key, value in request.model_dump(mode="json").items():
            setattr(item, key, value)

        await self.session.flush()

        return item

    async def get_item(self, item_id: uuid.UUID) -> Industry:
        item = await self.session.execute(
            select(Industry).where(Industry.id == item_id).options(selectinload(Industry.children))
        )

        item = item.scalars().one_or_none()

        if not item:
            raise HTTPException(status_code=404)

        return item

    async def delete_item(self, item_id: uuid.UUID):
        item = await self.get_item(item_id)

        await self.session.delete(item)

    async def get_industry_children(self, item_id: uuid.UUID) -> list[Industry]:
        item = await self.get_item(item_id)

        result = []

        for child in item.children:
            result.append(child)
            children = await self.get_industry_children(child.id)
            result.extend(children)

        return result
