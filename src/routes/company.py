import uuid

from fastapi import APIRouter

from ..core import VerifiedRequest
from ..dto import CompanyPostRequest, CompanyPutRequest, CompanyGetResponse

router = APIRouter(prefix="/companies")


@router.post("/")
async def create_item(
    request: CompanyPostRequest,
    _: VerifiedRequest
) -> CompanyGetResponse:
    ...


@router.put("/{item_id:uuid}")
async def update_item(
    item_id: uuid.UUID,
    request: CompanyPutRequest,
    _: VerifiedRequest
) -> CompanyGetResponse:
    ...


@router.get("/{item_id:uuid}")
async def get_item(
    item_id: uuid.UUID,
    _: VerifiedRequest
) -> CompanyGetResponse:
    ...


@router.delete("/{item_id:uuid}")
async def delete_item(
    item_id: uuid.UUID,
    _: VerifiedRequest
):
    ...
