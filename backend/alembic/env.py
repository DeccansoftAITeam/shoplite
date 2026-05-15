from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

from app.core.db import Base, engine
from app.modules.catalog import models as catalog_models  # noqa: F401
from app.modules.cart import models as cart_models  # noqa: F401
from app.modules.orders import models as orders_models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    # Offline mode not used in this project; kept for completeness.
    raise NotImplementedError("Run migrations online (requires a live DB connection).")


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
