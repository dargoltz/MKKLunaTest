import uuid

from fastapi import APIRouter, Depends, HTTPException, Response

from ..core import VerifiedRequest
from ..dto import BuildingPostRequest, BuildingGetResponse
from ..mappers import building_to_response
from ..service import BuildingService

router = APIRouter(prefix="/buildings")


@router.post("/")
async def create_item(
    request: BuildingPostRequest,
    _: VerifiedRequest,
    service: BuildingService = Depends(),
) -> BuildingGetResponse:
    item = await service.create_item(request)

    return building_to_response(item)


@router.get("/{item_id:uuid}")
async def get_item(
    item_id: uuid.UUID,
    _: VerifiedRequest,
    service: BuildingService = Depends(),
) -> BuildingGetResponse | None:
    item = await service.get_item(item_id)

    if not item:
        raise HTTPException(status_code=404)

    return building_to_response(item)


@router.delete("/{item_id:uuid}")
async def delete_item(
    item_id: uuid.UUID,
    _: VerifiedRequest,
    service: BuildingService = Depends(),
):
    await service.delete_item(item_id)

    return Response(status_code=204)
