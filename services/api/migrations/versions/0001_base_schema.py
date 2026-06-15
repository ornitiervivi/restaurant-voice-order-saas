"""Create base restaurant ordering schema.

Revision ID: 0001_base_schema
Revises:
Create Date: 2026-06-15
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_base_schema"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create tenant-scoped base tables for the MVP order lifecycle."""

    op.create_table(
        "restaurants",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("slug", name="uq_restaurants_slug"),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), primary_key=True),
        sa.Column("restaurant_id", sa.BigInteger(), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("role", sa.String(length=24), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("role IN ('admin', 'waiter', 'kitchen', 'bar')", name="ck_users_role"),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("restaurant_id", "id", name="uq_users_restaurant_id"),
        sa.UniqueConstraint("restaurant_id", "email", name="uq_users_restaurant_email"),
    )
    op.create_index("ix_users_restaurant_role", "users", ["restaurant_id", "role"])

    op.create_table(
        "restaurant_tables",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), primary_key=True),
        sa.Column("restaurant_id", sa.BigInteger(), nullable=False),
        sa.Column("label", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_restaurant_tables_status"),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("restaurant_id", "id", name="uq_restaurant_tables_restaurant_id"),
        sa.UniqueConstraint("restaurant_id", "label", name="uq_restaurant_tables_restaurant_label"),
    )
    op.create_index("ix_restaurant_tables_restaurant_status", "restaurant_tables", ["restaurant_id", "status"])

    op.create_table(
        "products",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), primary_key=True),
        sa.Column("restaurant_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("station", sa.String(length=24), nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("station IN ('kitchen', 'bar')", name="ck_products_station"),
        sa.CheckConstraint("price_cents >= 0", name="ck_products_price_cents_non_negative"),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("restaurant_id", "id", name="uq_products_restaurant_id"),
        sa.UniqueConstraint("restaurant_id", "name", name="uq_products_restaurant_name"),
    )
    op.create_index("ix_products_restaurant_station", "products", ["restaurant_id", "station"])
    op.create_index("ix_products_restaurant_available", "products", ["restaurant_id", "is_available"])

    op.create_table(
        "orders",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), primary_key=True),
        sa.Column("restaurant_id", sa.BigInteger(), nullable=False),
        sa.Column("table_id", sa.BigInteger(), nullable=False),
        sa.Column("opened_by_user_id", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="open"),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("status IN ('open', 'closed', 'cancelled')", name="ck_orders_status"),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["restaurant_id", "table_id"],
            ["restaurant_tables.restaurant_id", "restaurant_tables.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["restaurant_id", "opened_by_user_id"],
            ["users.restaurant_id", "users.id"],
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("restaurant_id", "id", name="uq_orders_restaurant_id"),
    )
    op.create_index("ix_orders_restaurant_status", "orders", ["restaurant_id", "status"])
    op.create_index("ix_orders_restaurant_table_status", "orders", ["restaurant_id", "table_id", "status"])

    op.create_table(
        "order_items",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), primary_key=True),
        sa.Column("restaurant_id", sa.BigInteger(), nullable=False),
        sa.Column("order_id", sa.BigInteger(), nullable=False),
        sa.Column("product_id", sa.BigInteger(), nullable=False),
        sa.Column("confirmed_by_user_id", sa.BigInteger(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price_cents", sa.Integer(), nullable=False),
        sa.Column("station", sa.String(length=24), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="confirmed"),
        sa.Column("modifiers", sa.Text(), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        sa.CheckConstraint("unit_price_cents >= 0", name="ck_order_items_unit_price_cents_non_negative"),
        sa.CheckConstraint("station IN ('kitchen', 'bar')", name="ck_order_items_station"),
        sa.CheckConstraint(
            "status IN ('confirmed', 'preparing', 'ready', 'delivered', 'cancelled')",
            name="ck_order_items_status",
        ),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["restaurant_id", "order_id"],
            ["orders.restaurant_id", "orders.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["restaurant_id", "product_id"],
            ["products.restaurant_id", "products.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["restaurant_id", "confirmed_by_user_id"],
            ["users.restaurant_id", "users.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_order_items_restaurant_order", "order_items", ["restaurant_id", "order_id"])
    op.create_index("ix_order_items_restaurant_station_status", "order_items", ["restaurant_id", "station", "status"])


def downgrade() -> None:
    """Drop base schema in dependency order."""

    op.drop_index("ix_order_items_restaurant_station_status", table_name="order_items")
    op.drop_index("ix_order_items_restaurant_order", table_name="order_items")
    op.drop_table("order_items")
    op.drop_index("ix_orders_restaurant_table_status", table_name="orders")
    op.drop_index("ix_orders_restaurant_status", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_products_restaurant_available", table_name="products")
    op.drop_index("ix_products_restaurant_station", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_restaurant_tables_restaurant_status", table_name="restaurant_tables")
    op.drop_table("restaurant_tables")
    op.drop_index("ix_users_restaurant_role", table_name="users")
    op.drop_table("users")
    op.drop_table("restaurants")
