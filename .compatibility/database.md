# Database compatibility

Use PostgreSQL unless a project decision changes this. Track migrations, indexes and driver constraints here.

## T-003 PostgreSQL baseline

- Local development uses `postgres:16-alpine` in Docker Compose.
- Backend configuration exposes the database connection through `API_DATABASE_URL`.
- Schema, migrations, constraints and tenant indexes remain deferred to T-004.
