# DECISIONS.md

## Decision log

| ID | Date | Decision | Reason | Impact |
|---|---|---|---|---|
| D-001 | 2026-06-15 | Repository name: restaurant-voice-order-saas | Clear product intent | Used for project bootstrap |
| D-002 | 2026-06-15 | AI requires human confirmation before submit | Prevents incorrect orders and preserves waiter accountability | Mandatory UX/business rule across backend, mobile, web and realtime |
| D-003 | 2026-06-15 | Workana MVP stack candidates are Flutter, Flutter Web or equivalent frontend, Python FastAPI or Node.js, PostgreSQL, WebSocket and AI voice/STT/parser | Aligns harness with requested project stack before product planning | Guides compatibility and skill selection |
| D-004 | 2026-06-15 | Java/Spring remains template-only for this project unless explicitly selected later | Requested stack is Python FastAPI or Node.js for backend | Prevents Java/Spring from governing implementation by default |
| D-005 | 2026-06-15 | Select Python FastAPI as final MVP backend stack | FastAPI offers strong async API/WebSocket support, Pydantic validation, OpenAPI generation and lower AI/NLP integration friction than Node.js for this MVP | Backend tasks must use Python FastAPI compatibility gates; Node.js remains non-selected alternative |
| D-006 | 2026-06-15 | Use Flutter for Android waiter app and Flutter Web for MVP admin/kitchen/bar screens | Shared Dart/Flutter skillset and UI patterns reduce MVP delivery complexity | Web tasks should validate Flutter Web/browser constraints before implementation |
| D-007 | 2026-06-15 | Use PostgreSQL with migrations as source of truth | Order lifecycle, tenant isolation and auditability require relational consistency | Database tasks must define schema, constraints, indexes and migration validation |
| D-008 | 2026-06-15 | Use authenticated WebSocket as MVP realtime transport | Kitchen/bar and waiter status updates need low-latency bidirectional delivery | Realtime tasks must define channel auth, tenant isolation, ordering, idempotency and reconnect behavior |
| D-009 | 2026-06-15 | Isolate STT and parser behind application interfaces/adapters | Provider, cost, privacy and model choices may change | MVP can start with mock/demo adapters and later swap provider without domain changes |
| D-010 | 2026-06-15 | Plan implementation in small sequential, validable increments before coding | Reduces risk and keeps Workana MVP scope controlled | TASKS.md is the executable backlog and implementation must follow dependency order |
| D-011 | 2026-06-15 | Enforce explicit backend responsibility boundaries for domain, use cases, ports, gateways/adapters and infrastructure | Reviewer concern clarified that `services/api` is a deployable folder name, not a license for mixed service classes | Future backend tasks must keep HTTP/WebSocket/provider/database code out of domain/use-case decisions and route all business behavior through use cases and ports |
| D-012 | 2026-06-15 | Bootstrap FastAPI backend with Python >=3.11, FastAPI >=0.115,<1.0, Pydantic Settings >=2.7,<3.0, Uvicorn >=0.34,<1.0 and pytest/httpx for tests | Establishes the smallest runnable API base while keeping future PostgreSQL, auth, WebSocket and AI adapters outside domain code | Backend base now exposes `/health`; dependency installation may require package-index access in local/CI environments |
| D-013 | 2026-06-15 | Use PostgreSQL 16 Alpine image for local T-003 Docker Compose and expose the API database URL via `API_DATABASE_URL` | Keeps the local database explicit, lightweight and aligned with the selected PostgreSQL source-of-truth decision while deferring migrations/schema to T-004 | Future database work can consume the same environment setting; secrets remain local-development placeholders only |
| D-014 | 2026-06-15 | Standardize task-based pull request titles as `T-###: Imperative summary` | Prevents inconsistent PR naming across agent runs and keeps review history searchable by task ID | Future PRs must use the task ID prefix when tied to `TASKS.md`; non-task correction PRs should use `CHORE:` unless instructed otherwise |
| D-015 | 2026-06-15 | Use Alembic with SQLAlchemy and psycopg for PostgreSQL migrations/database connectivity | This is the standard Python/FastAPI ecosystem path for versioned schema changes and PostgreSQL access while preserving infrastructure boundaries | T-004 base schema is managed by Alembic; future persistence adapters must keep tenant-scoped constraints and migration validation current |
| D-016 | 2026-06-15 | Implement MVP authentication with PBKDF2-HMAC-SHA256 password hashes, signed HS256 JWT access/refresh tokens, and tenant/role authorization use cases | Keeps authentication dependency-light for the current environment while preserving secure defaults and explicit application boundaries | Future persistent user management in T-006 must replace the local in-memory demo repository without changing auth use-case contracts |

## Deferred decisions before implementation tasks

| Topic | Decision needed before coding | Suggested owner |
|---|---|---|
| Python/FastAPI versions and dependency manager | Python version, FastAPI version, uv/poetry/pip-tools choice | Backend Engineer + DevOps Engineer |
| Auth details | Token TTLs, refresh storage, password policy and initial admin bootstrap | Backend Engineer + Security Reviewer |
| STT provider | Provider/model, language, retention, latency and cost | AI/Voice Engineer + Product Analyst |
| Parser provider | LLM/rules/hybrid approach, confidence thresholds and fallback UX | AI/Voice Engineer |
| WebSocket scaling | In-memory MVP vs Redis/pubsub for multi-instance deployment | Solution Architect + DevOps Engineer |
