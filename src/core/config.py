from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str = ... # todo

config = Config()