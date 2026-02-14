import uuid
from pydantic import BaseModel, field_validator


class CompanyPostRequest(BaseModel):
    name: str
    phone_numbers: list[str]
    building_id: uuid.UUID

    @field_validator("phone_numbers", mode="before")
    def validate_phone_numbers(cls, v):
        if not v:
            raise ValueError("Phone numbers are required")

        for phone in v:
            if len(phone) != 12 or phone[0] != "+" or not phone[1:].isdigit():
                raise ValueError("Phone number must consist of the + symbol and 11 digits.")

class CompanyPutRequest(CompanyPostRequest):
    pass

class CompanyGetResponse(BaseModel):
    id: uuid.UUID
    name: str
    industry_names: list[str]
    address: str
    phone_numbers: list[str]

