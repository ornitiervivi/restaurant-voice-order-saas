# Local PostgreSQL

TASK T-003 adds the local PostgreSQL service used by future migration and repository tasks.

## Development defaults

The Compose file uses safe local-development defaults when variables are not provided:

- database: `restaurant_voice_order`
- user: `restaurant_voice_order`
- password: `restaurant_voice_order_dev_password`
- host port: `5432`

These values are for local development only. Do not reuse them in production or shared environments.

## Commands

From the repository root:

```bash
docker compose -f infra/docker-compose.yml config
docker compose -f infra/docker-compose.yml up -d postgres
docker compose -f infra/docker-compose.yml ps
```

The API service is available under the optional Compose profile `api` for development once Python dependencies can be installed:

```bash
docker compose -f infra/docker-compose.yml --profile api up api
```

## Data lifecycle

PostgreSQL data is stored in the named volume `restaurant-voice-order-saas_postgres_data` unless the Compose project name is overridden. Remove the volume only when intentionally resetting local data.
