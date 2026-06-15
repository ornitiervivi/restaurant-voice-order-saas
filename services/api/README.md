# API service

Python FastAPI backend for the restaurant voice ordering SaaS MVP.

## Current increment

T-003 extends the API service configuration with local PostgreSQL environment support. T-002 bootstrapped the API service with:

- FastAPI application factory in `src/main.py`.
- Lightweight `/health` endpoint that does not require PostgreSQL or external providers.
- Environment-driven settings in `src/infrastructure/settings.py`, including `API_DATABASE_URL` for future PostgreSQL integration.
- Clean Architecture folders for `domain`, `application`, `adapters` and `infrastructure`.
- Pytest-based health check coverage.

## Local validation

```bash
pytest
python -m compileall src tests
```

From the repository root, validate the local PostgreSQL Compose configuration:

```bash
docker compose -f infra/docker-compose.yml config
docker compose -f infra/docker-compose.yml up -d postgres
docker compose -f infra/docker-compose.yml ps
```

## Architecture rules

Business behavior must stay outside HTTP routes and infrastructure wiring. Future voice/STT/parser outputs remain drafts until an authenticated waiter confirms the order.
