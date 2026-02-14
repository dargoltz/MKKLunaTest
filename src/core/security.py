from typing import Annotated
from fastapi import HTTPException, Depends, Header

from .config import config

async def get_api_key(key: str = Header(...)) -> str:
    return key

async def verify_api_key(key: str = Depends(get_api_key)):
    if key != config.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


VerifiedRequest = Annotated[str, Depends(verify_api_key)]
