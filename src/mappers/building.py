from ..dto import BuildingGetResponse
from ..models import Building


def building_to_response(building: Building) -> BuildingGetResponse:
    return BuildingGetResponse(
        id=building.id,
        address=building.address,
        latitude=building.latitude,
        longitude=building.longitude
    )
