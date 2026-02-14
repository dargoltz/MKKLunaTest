from ..models import Industry

from ..dto import IndustryGetResponse


def industry_to_response(industry: Industry) -> IndustryGetResponse:
    return IndustryGetResponse(
        id=industry.id,
        name=industry.name,
    )
