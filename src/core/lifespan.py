from contextlib import asynccontextmanager
from fastapi import FastAPI

from .db import database_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_manager.init_db()
    yield
    await database_manager.close_db()