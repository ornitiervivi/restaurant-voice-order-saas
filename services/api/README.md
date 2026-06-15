# API service

Python FastAPI backend for the restaurant voice ordering SaaS MVP.

## Current increment

T-002 bootstraps the API service with:

- FastAPI application factory in `src/main.py`.
- Lightweight `/health` endpoint that does not require PostgreSQL or external providers.
- Environment-driven settings in `src/infrastructure/settings.py`.
- Clean Architecture folders for `domain`, `application`, `adapters` and `infrastructure`.
- Pytest-based health check coverage.

## Local validation

```bash
pytest
python -m compileall src tests
```

## Architecture rules

Business behavior must stay outside HTTP routes and infrastructure wiring. Future voice/STT/parser outputs remain drafts until an authenticated waiter confirms the order.
