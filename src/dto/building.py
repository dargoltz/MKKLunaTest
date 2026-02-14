import uuid
from pydantic import BaseModel, Field, field_validator


class BuildingPostRequest(BaseModel):
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-90, le=90)

    @field_validator("latitude", "longitude", mode="before")
    def round_coordinate(cls, v):
        return round(v, 6)


class BuildingPutRequest(BuildingPostRequest):
    pass


class BuildingGetResponse(BaseModel):
    id: uuid.UUID
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-90, le=90)
