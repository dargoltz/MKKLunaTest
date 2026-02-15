import uuid
from pydantic import BaseModel, field_validator


class CompanyPostRequest(BaseModel):
    name: str
    phone_numbers: list[str]
    building_id: uuid.UUID
    industry_ids: list[uuid.UUID]

    @field_validator("phone_numbers", mode="before")
    def validate_phone_numbers(cls, v):
        if not v:
            raise ValueError("Phone numbers are required")

        for phone in v:
            if len(phone) != 12 or phone[0] != "+" or not phone[1:].isdigit():
                raise ValueError("Phone number must consist of the + symbol and 11 digits.")

        return v

    @field_validator("industry_ids", mode="before")
    def validate_industry_ids(cls, v):
        if not v:
            raise ValueError("Industry IDs are required")

        return v


class CompanyPutRequest(CompanyPostRequest):
    name: str | None = None
    phone_numbers: list[str] | None = None
    building_id: uuid.UUID | None = None
    industry_ids: list[uuid.UUID] | None = None

    @field_validator("phone_numbers", mode="before")
    def validate_phone_numbers(cls, v):
        if v is None:
            return v
        else:
            if len(v) == 0:
                raise ValueError("Phone numbers are required")
            else:
                for phone in v:
                    if len(phone) != 12 or phone[0] != "+" or not phone[1:].isdigit():
                        raise ValueError("Phone number must consist of the + symbol and 11 digits.")

        return v


class CompanyGetResponse(BaseModel):
    id: uuid.UUID
    name: str
    industry_names: list[str]
    address: str
    phone_numbers: list[str]
