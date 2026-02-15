from fastapi import FastAPI

from src.core import lifespan, VerifiedRequest
from src.routes import api_router

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
