from ..models import Company

from ..dto import CompanyGetResponse


def company_to_response(company: Company) -> CompanyGetResponse:
    return CompanyGetResponse(
        id=company.id,
        name=company.name,
        industry_names=[industry.name for industry in company.industries],
        address=company.building.address,
        phone_numbers=company.phone_numbers
    )
