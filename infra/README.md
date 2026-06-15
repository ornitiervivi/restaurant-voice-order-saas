# Infrastructure

Local development infrastructure for the restaurant voice ordering SaaS.

## Current state

TASK T-003 adds Docker Compose configuration for a local PostgreSQL service and an optional API development service profile.

## Intended responsibilities

- Local Docker Compose environment in `docker-compose.yml`.
- PostgreSQL service configuration for development in `postgres/README.md`.
- Seed data and demo environment support.
- Operational documentation for local validation.

## Safety notes

- Do not commit real secrets.
- Demo credentials must be local-development only.
- Realtime and database services must preserve tenant isolation.

## T-003 validation commands

```bash
docker compose -f infra/docker-compose.yml config
docker compose -f infra/docker-compose.yml up -d postgres
docker compose -f infra/docker-compose.yml ps
```
