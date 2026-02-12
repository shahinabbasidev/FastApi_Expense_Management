import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# -------------------------------------------------
# Load .env BEFORE importing anything that uses Settings
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    print(
        "Warning: .env file not found. Falling back to system environment variables."
    )

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("SQLALCHEMY_DATABASE_URL is not set")

# -------------------------------------------------
# Alembic config
# -------------------------------------------------
config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url from env
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# -------------------------------------------------
# Import models AFTER env is loaded
# -------------------------------------------------
from core.database import Base
from users.models import *
from expenses.models import *

target_metadata = Base.metadata


# -------------------------------------------------
# Migration runners
# -------------------------------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
