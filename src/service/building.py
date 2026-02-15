import math
import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

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
        await self.session.refresh(item)

        return item

    async def get_item(self, item_id: uuid.UUID) -> Building:
        item = await self.session.execute(
            select(Building).where(Building.id == item_id)
        )

        item = item.scalars().one_or_none()

        if not item:
            raise HTTPException(status_code=404)

        return item

    async def delete_item(self, item_id: uuid.UUID) -> None:
        item = await self.get_item(item_id)

        await self.session.delete(item)

    async def get_in_radius(self, latitude: float, longitude: float, radius: int) -> list[Building]:
        delta_lat = radius / 111
        delta_lon = radius / (111 * math.cos(math.radians(latitude)))

        query = await self.session.execute(
            select(Building).where(
                and_(
                    Building.latitude.between(latitude - delta_lat, latitude + delta_lat),
                    Building.longitude.between(longitude - delta_lon, longitude + delta_lon)
                )
            ).options(selectinload(Building.companies))
        )

        items = query.scalars().all()

        return list(items)
