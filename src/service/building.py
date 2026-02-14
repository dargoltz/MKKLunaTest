import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import database_manager
from ..dto import BuildingPostRequest
from ..models import Building


class BuildingService:
    def __init__(self, session: AsyncSession = Depends(database_manager.get_db)):
        self.session = session

    async def create_item(self, request: BuildingPostRequest) -> Building:
        item = Building(
            address=request.address,
            latitude=request.latitude,
            longitude=request.longitude
        )

        self.session.add(item)
        await self.session.flush()

        return item

    async def get_item(self, item_id: uuid.UUID) -> Building:
        item = await self.session.get(Building, item_id)

        if not item:
            raise HTTPException(status_code=404)

        return item

    async def delete_item(self, item_id: uuid.UUID) -> None:
        item = await self.get_item(item_id)

        await self.session.delete(item)
