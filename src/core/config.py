from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str = "postgres:postgres@localhost:5432/postgres"
    API_KEY: str = "SERIOUS_CYBER_DEFENSE"

config = Config()