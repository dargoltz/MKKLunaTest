
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing_extensions import AsyncGenerator

from .config import config
from .logger import logger

DB_ASYNC_DRIVER = "postgresql+asyncpg://"

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.session_maker = None

    async def add_engine(self):
        self.engine = create_async_engine(
            url=f"{DB_ASYNC_DRIVER}{config.DB_URL}",
            future=True,
            pool_size=20,
            max_overflow=5,
        )

        # noinspection PyTypeChecker
        self.session_maker = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        await self.add_engine()

    async def close_db(self):
        await self.engine.dispose()
        logger.info(f"DB closed")

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    yield session
                except Exception as ex:
                    logger.error(f"DB error: {ex}")
                    await session.rollback() # todo check maybe extra
                    raise
                finally:
                    pass


database_manager = DatabaseManager()
