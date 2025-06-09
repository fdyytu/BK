from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

from .connection import Base
from .settings import SQLALCHEMY_DATABASE_URL

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations():
    """Run migrations in 'online' mode."""
    connectable = create_engine(SQLALCHEMY_DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()