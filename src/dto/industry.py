import uuid

from pydantic import BaseModel


class IndustryPostRequest(BaseModel):
    name: str
    parent_id: uuid.UUID | None = None


class IndustryPutRequest(IndustryPostRequest):
    pass


class IndustryGetResponse(BaseModel):
    id: uuid.UUID
    name: str
