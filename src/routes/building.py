import uuid

from fastapi import APIRouter

from ..core import VerifiedRequest
from ..dto import BuildingPostRequest, BuildingPutRequest, BuildingGetResponse

router = APIRouter(prefix="/buildings")


@router.post("/")
async def create_item(
    request: BuildingPostRequest,
    _: VerifiedRequest
) -> BuildingGetResponse:
    ...


@router.put("/{item_id:uuid}")
async def update_item(
    item_id: uuid.UUID,
    request: BuildingPutRequest,
    _: VerifiedRequest
) -> BuildingGetResponse:
    ...


@router.get("/{item_id:uuid}")
async def get_item(
    item_id: uuid.UUID,
    _: VerifiedRequest
) -> BuildingGetResponse:
    ...


@router.delete("/{item_id:uuid}")
async def delete_item(
    item_id: uuid.UUID,
    _: VerifiedRequest
):
    ...
