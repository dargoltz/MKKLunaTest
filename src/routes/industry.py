import uuid

from fastapi import APIRouter, Depends, Response

from ..core import VerifiedRequest
from ..dto import IndustryPostRequest, IndustryPutRequest, IndustryGetResponse
from ..mappers import industry_to_response
from ..service import IndustryService

router = APIRouter(prefix="/industries")


@router.post("/")
async def create_item(
    request: IndustryPostRequest,
    _: VerifiedRequest,
    service: IndustryService = Depends(),
) -> IndustryGetResponse:
    item = await service.create_item(request)

    return industry_to_response(item)


@router.put("/{item_id:uuid}")
async def update_item(
    item_id: uuid.UUID,
    request: IndustryPutRequest,
    _: VerifiedRequest,
    service: IndustryService = Depends(),
) -> IndustryGetResponse:
    item = await service.update_item(item_id, request)

    return industry_to_response(item)


@router.get("/{item_id:uuid}")
async def get_item(
    item_id: uuid.UUID,
    _: VerifiedRequest,
    service: IndustryService = Depends(),
) -> IndustryGetResponse:
    item = await service.get_item(item_id)

    return industry_to_response(item)


@router.delete("/{item_id:uuid}")
async def delete_item(
    item_id: uuid.UUID,
    _: VerifiedRequest,
    service: IndustryService = Depends(),
):
    await service.delete_item(item_id)
    return Response(status_code=204)
