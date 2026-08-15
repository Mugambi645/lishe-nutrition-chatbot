from logging.config import fileConfig
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import create_async_engine

# 1. Force Python to see the root directory (services/api)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# 2. Import app settings and models
from app.config import settings
from app.models import Base

config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Inject dynamic database URL (cast to str for Pydantic/URL objects)
raw_db_url = str(settings.database_url)
# If the application uses an async driver (e.g. asyncpg), Alembic should use a sync driver
# for autogenerate. Convert an async URL like 'postgresql+asyncpg://...' to a sync URL
# by removing the '+asyncpg' suffix. Adjust if you prefer a specific sync driver.
if "+asyncpg" in raw_db_url:
    sync_db_url = raw_db_url.replace("+asyncpg", "")
else:
    sync_db_url = raw_db_url

config.set_main_option("sqlalchemy.url", sync_db_url)

# 4. Connect Base metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Use an AsyncEngine for the app's async DB driver and run migrations
    # in a sync context via `run_sync`.
    # Use the original async DB URL so the asyncpg dialect/driver is used.
    connectable = create_async_engine(
        raw_db_url,
        poolclass=pool.NullPool,
    )

    def run_sync_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    import asyncio

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(run_sync_migrations)

    asyncio.run(do_run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()