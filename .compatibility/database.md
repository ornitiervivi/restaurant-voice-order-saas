# Database compatibility

Use PostgreSQL unless a project decision changes this. Track migrations, indexes and driver constraints here.

## T-003 PostgreSQL baseline

- Local development uses `postgres:16-alpine` in Docker Compose.
- Backend configuration exposes the database connection through `API_DATABASE_URL`.
- Schema, migrations, constraints and tenant indexes remain deferred to T-004.


## T-004 migration baseline

- Migration tooling uses Alembic with SQLAlchemy and psycopg for PostgreSQL connectivity.
- Base tables are `restaurants`, `users`, `restaurant_tables`, `products`, `orders` and `order_items`.
- Tenant-owned child tables include `restaurant_id`, tenant lookup indexes and composite foreign keys where needed to prevent cross-restaurant order references.
