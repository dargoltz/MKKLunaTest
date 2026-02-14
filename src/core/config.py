from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mkklunatest"
    API_KEY: str = "SERIOUS_CYBER_DEFENSE"

config = Config()