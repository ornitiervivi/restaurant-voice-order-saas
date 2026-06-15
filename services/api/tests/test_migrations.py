"""Migration validation tests for the base PostgreSQL schema."""

from pathlib import Path

import pytest

MIGRATION_PATH = Path(__file__).resolve().parents[1] / "migrations" / "versions" / "0001_base_schema.py"


@pytest.mark.parametrize(
    "table_name",
    [
        "restaurants",
        "users",
        "restaurant_tables",
        "products",
        "orders",
        "order_items",
    ],
)
def test_base_migration_defines_required_tables(table_name: str) -> None:
    """The first migration creates every MVP base table."""

    migration = MIGRATION_PATH.read_text(encoding="utf-8")

    assert f'create_table(\n        "{table_name}"' in migration


@pytest.mark.parametrize(
    "constraint_name",
    [
        "uq_users_restaurant_email",
        "uq_restaurant_tables_restaurant_label",
        "uq_products_restaurant_name",
        "ix_orders_restaurant_table_status",
        "ix_order_items_restaurant_station_status",
        "ck_order_items_quantity_positive",
    ],
)
def test_base_migration_defines_tenant_lookup_constraints(constraint_name: str) -> None:
    """Tenant-scoped uniqueness, lookup indexes and value checks are explicit."""

    migration = MIGRATION_PATH.read_text(encoding="utf-8")

    assert constraint_name in migration


@pytest.mark.parametrize(
    "composite_reference",
    [
        '["restaurant_id", "table_id"]',
        '["restaurant_id", "opened_by_user_id"]',
        '["restaurant_id", "order_id"]',
        '["restaurant_id", "product_id"]',
        '["restaurant_id", "confirmed_by_user_id"]',
    ],
)
def test_base_migration_prevents_cross_tenant_references(composite_reference: str) -> None:
    """Child rows must reference parent rows through the same restaurant scope."""

    migration = MIGRATION_PATH.read_text(encoding="utf-8")

    assert composite_reference in migration


def test_database_engine_uses_configured_database_url() -> None:
    """Infrastructure exposes a SQLAlchemy engine factory for adapters."""

    sqlalchemy = pytest.importorskip("sqlalchemy")

    from src.infrastructure.database.engine import create_database_engine
    from src.infrastructure.settings import Settings

    settings = Settings(database_url="postgresql+psycopg://user:pass@localhost:5432/db")
    engine = create_database_engine(settings)

    assert isinstance(engine, sqlalchemy.Engine)
    assert str(engine.url) == "postgresql+psycopg://user:***@localhost:5432/db"
