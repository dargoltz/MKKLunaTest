from logging.config import fileConfig
from alembic import context

from src.core import config as app_config
from src.models import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

DB_SYNC_DRIVER = "postgresql+psycopg2://"
DB_URL = f"postgresql+psycopg2://{app_config.DB_URL}"

def run_migrations_offline() -> None:
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine
    connectable = create_engine(DB_URL)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
