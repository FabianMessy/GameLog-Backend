from logging.config import fileConfig
from pathlib import Path
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

ROOT_DIR = Path(__file__).resolve().parents[3]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


from sqlmodel import SQLModel
from app.core.config import settings

import app.models


# Metadata utilizada pelo autogenerate
target_metadata = SQLModel.metadata


config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
)


def run_migrations_offline() -> None:
    """Executa migrations em modo offline."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa migrations conectando ao banco."""

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
