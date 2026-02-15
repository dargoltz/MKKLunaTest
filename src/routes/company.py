import uuid

from fastapi import APIRouter, Depends, Response

from ..core import VerifiedRequest
from ..dto import CompanyPostRequest, CompanyPutRequest, CompanyGetResponse
from ..mappers import company_to_response
from ..service import CompanyService

router = APIRouter(prefix="/companies")


@router.post("/")
async def create_item(
    request: CompanyPostRequest,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
) -> CompanyGetResponse:
    item = await service.create_item(request)

    return company_to_response(item)


@router.put("/{item_id:uuid}")
async def update_item(
    item_id: uuid.UUID,
    request: CompanyPutRequest,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
) -> CompanyGetResponse:
    item = await service.update_item(item_id, request)

    return company_to_response(item)


@router.get("/{item_id:uuid}")
async def get_item(
    item_id: uuid.UUID,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
) -> CompanyGetResponse:
    item = await service.get_item(item_id)

    return company_to_response(item)


@router.delete("/{item_id:uuid}")
async def delete_item(
    item_id: uuid.UUID,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
):
    await service.delete_item(item_id)
    return Response(status_code=204)


@router.get("/search/{search}")
async def get_by_name(
    name: str,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
) -> CompanyGetResponse:
    item = await service.get_by_name(name)
    return company_to_response(item)


@router.get("/by-coordinate")
async def get_by_coordinate(
    latitude: float,
    longitude: float,
    radius: int,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
) -> list[CompanyGetResponse]:
    items = await service.get_by_coordinate(latitude, longitude, radius)
    return [company_to_response(item) for item in items]


@router.get("/by-building/{building_id:uuid}")
async def get_by_building(
    building_id: uuid.UUID,
    _: VerifiedRequest,
    service: CompanyService = Depends(),
) -> list[CompanyGetResponse]:
    items = await service.get_by_building(building_id)
    return [company_to_response(item) for item in items]


@router.get("/by-industry/{industry_id:uuid}")
async def get_by_industry(
    industry_id: uuid.UUID,
    _: VerifiedRequest,
    strict: bool = False,
    service: CompanyService = Depends(),
) -> list[CompanyGetResponse]:
    items = await service.get_by_industry(industry_id, strict)
    return [company_to_response(item) for item in items]
