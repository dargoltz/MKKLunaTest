import uuid

from fastapi import APIRouter

from ..core import VerifiedRequest
from ..dto import IndustryPostRequest, IndustryPutRequest, IndustryGetResponse

router = APIRouter(prefix="/industries")


@router.post("/")
async def create_item(
    request: IndustryPostRequest,
    _: VerifiedRequest
) -> IndustryGetResponse:
    ...


@router.put("/{item_id:uuid}")
async def update_item(
    item_id: uuid.UUID,
    request: IndustryPutRequest,
    _: VerifiedRequest
) -> IndustryGetResponse:
    ...


@router.get("/{item_id:uuid}")
async def get_item(
    item_id: uuid.UUID,
    _: VerifiedRequest
) -> IndustryGetResponse:
    ...


@router.delete("/{item_id:uuid}")
async def delete_item(
    item_id: uuid.UUID,
    _: VerifiedRequest
):
    ...
