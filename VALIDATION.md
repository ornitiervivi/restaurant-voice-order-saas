# VALIDATION.md

## Validation strategy

Every implementation must define and run applicable validation. Documentation-only changes must at minimum pass repository text checks such as `git diff --check`.

## Minimum checks

- Backend tests for the selected FastAPI or Node.js stack.
- Frontend/mobile tests when Flutter or web UI changes are applicable.
- Static analysis/lint when available.
- Database migration validation for PostgreSQL changes.
- Docker Compose startup when local runtime changes are relevant.
- Manual demo path for voice order confirmation.
- Realtime event delivery validation.

## Stack-specific validation prompts

- Flutter: validate Android build/test path, microphone permission behavior and WebSocket client behavior when relevant.
- Flutter Web or equivalent frontend: validate target browser support and kitchen/bar realtime display behavior.
- Python FastAPI: validate API tests, schema validation, async behavior and WebSocket endpoints when relevant.
- Node.js: validate TypeScript build, unit/integration tests, schema validation and WebSocket endpoints when relevant.
- PostgreSQL: validate migrations, constraints, transaction boundaries and tenant isolation when relevant.
- AI voice: validate STT/parser fixtures, ambiguity handling and confirmation-gate enforcement.
- Realtime: validate auth, reconnect, idempotency, ordering and delivery failure handling.

## Critical acceptance validation

AI-generated orders must require human confirmation before submission. Any implementation that submits, persists as submitted or emits AI-parsed orders without human confirmation fails validation.

## T-002 validation notes

- Backend base validation commands are `cd services/api && pytest`, `cd services/api && python -m compileall src tests` and `git diff --check`.
- In this execution environment, package installation from the external Python package index was blocked with HTTP 403 while trying to install build dependencies. Tests are present and will execute the FastAPI health check when dependencies are available; without FastAPI installed, pytest reports the dependency as skipped rather than hiding an implementation failure.


## T-003 validation notes

- Local infrastructure validation commands are `docker compose -f infra/docker-compose.yml config`, `docker compose -f infra/docker-compose.yml up -d postgres`, `docker compose -f infra/docker-compose.yml ps`, and `git diff --check`.
- The PostgreSQL container uses local-development credentials from `infra/docker-compose.yml`/`services/api/.env.example`; no production secrets are committed.
- The API Compose service is intentionally behind the optional `api` profile because T-003 only requires PostgreSQL startup, while full API containerization is deferred to T-020.
