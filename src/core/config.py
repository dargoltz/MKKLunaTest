from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mkklunatest"

config = Config()