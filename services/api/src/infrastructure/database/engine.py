"""Database engine factory for infrastructure adapters."""

from sqlalchemy import Engine, create_engine

from src.infrastructure.settings import Settings


def create_database_engine(settings: Settings) -> Engine:
    """Create a SQLAlchemy engine from runtime settings."""

    return create_engine(settings.database_url, pool_pre_ping=True)
