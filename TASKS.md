# TASKS.md

## Backlog format

Each task contains: ID, objetivo, arquivos esperados, critérios de aceite, comandos de validação, dependências and status.

## Executable MVP backlog

### T-000 - Planning and SDD baseline

- ID: T-000
- objetivo: Consolidate Workana MVP scope, final stack decision, architecture plan and executable backlog without implementing code.
- arquivos esperados:
  - PROJECT_CONTEXT.md
  - SPEC.md
  - ARCHITECTURE.md
  - DECISIONS.md
  - PLAN.md
  - TASKS.md
- critérios de aceite:
  - Backend stack decision between FastAPI and Node.js is recorded with technical justification.
  - Plan covers monorepo, backend, PostgreSQL, auth, CRUD, order lifecycle, Flutter Android, web/admin, kitchen/bar realtime, WebSocket, voice, STT, parser, confirmation, tests, Docker Compose, demo data and final validation.
  - No product implementation code is added.
- comandos de validação:
  - `git diff --check`
  - `git status --short`
- dependências: none
- status: done

### T-001 - Monorepo skeleton

- ID: T-001
- objetivo: Create the initial monorepo folder structure for backend, Flutter apps, shared packages and infrastructure.
- arquivos esperados:
  - apps/waiter_app/README.md
  - apps/web_console/README.md
  - services/api/README.md
  - packages/api_contracts/README.md
  - infra/README.md
  - README.md
- critérios de aceite:
  - Folder structure matches ARCHITECTURE.md.
  - No unsupported stack is introduced.
  - README documents local development intent and current no-code state.
- comandos de validação:
  - `git diff --check`
  - `find apps services packages infra -maxdepth 2 -type f | sort`
- dependências: T-000
- status: done

### T-002 - Backend FastAPI base

- ID: T-002
- objetivo: Bootstrap Python FastAPI backend with health endpoint, settings, test runner and clean architecture folders.
- arquivos esperados:
  - services/api/pyproject.toml
  - services/api/src/main.py
  - services/api/src/domain/
  - services/api/src/application/
  - services/api/src/adapters/
  - services/api/src/infrastructure/
  - services/api/tests/test_health.py
- critérios de aceite:
  - `/health` returns an OK response.
  - Tests run locally.
  - Architecture folders are present and documented.
- comandos de validação:
  - `cd services/api && pytest`
  - `cd services/api && python -m compileall src tests`
- dependências: T-001
- status: done

### T-003 - Docker Compose with PostgreSQL

- ID: T-003
- objetivo: Add local Docker Compose services for PostgreSQL and backend development.
- arquivos esperados:
  - infra/docker-compose.yml
  - services/api/.env.example
  - infra/postgres/README.md
- critérios de aceite:
  - PostgreSQL starts with configured database/user/password from examples.
  - Backend can receive database URL via environment variable.
  - Secrets are not committed.
- comandos de validação:
  - `docker compose -f infra/docker-compose.yml config`
  - `docker compose -f infra/docker-compose.yml up -d postgres`
  - `docker compose -f infra/docker-compose.yml ps`
- dependências: T-002
- status: done

### T-004 - PostgreSQL migrations and base schema

- ID: T-004
- objetivo: Configure migrations and create base relational schema for restaurants, users, tables, products, orders and order items.
- arquivos esperados:
  - services/api/migrations/
  - services/api/src/infrastructure/database/
  - services/api/tests/test_migrations.py
- critérios de aceite:
  - Migrations create all base tables with restaurant scoping.
  - Constraints and indexes cover tenant isolation and common lookup paths.
  - Migration validation passes against local PostgreSQL.
- comandos de validação:
  - `cd services/api && alembic upgrade head`
  - `cd services/api && alembic downgrade -1 && alembic upgrade head`
  - `cd services/api && pytest tests/test_migrations.py`
- dependências: T-003
- status: done

### T-005 - Authentication and role authorization

- ID: T-005
- objetivo: Implement email/password authentication, JWT token flow and role/tenant guards.
- arquivos esperados:
  - services/api/src/domain/user.py
  - services/api/src/application/auth/
  - services/api/src/adapters/http/auth_routes.py
  - services/api/src/infrastructure/security/
  - services/api/tests/test_auth.py
- critérios de aceite:
  - Users can log in with valid credentials.
  - Invalid credentials fail safely.
  - Role and restaurant scoping are enforced.
  - Passwords are hashed.
- comandos de validação:
  - `cd services/api && pytest tests/test_auth.py`
  - `cd services/api && pytest`
- dependências: T-004
- status: done

### T-006 - Restaurant, users, tables and products CRUD

- ID: T-006
- objetivo: Implement admin APIs for restaurant setup, users, tables and products.
- arquivos esperados:
  - services/api/src/application/admin/
  - services/api/src/adapters/http/admin_routes.py
  - services/api/tests/test_admin_crud.py
- critérios de aceite:
  - Admin can create/update/list/deactivate users, tables and products.
  - Products include station routing to kitchen/bar.
  - Tenant isolation tests pass.
- comandos de validação:
  - `cd services/api && pytest tests/test_admin_crud.py`
  - `cd services/api && pytest`
- dependências: T-005
- status: pending

### T-007 - Order lifecycle backend

- ID: T-007
- objetivo: Implement order/tab open, resume, confirmed item insertion, status updates, history and close flow.
- arquivos esperados:
  - services/api/src/domain/order.py
  - services/api/src/application/orders/
  - services/api/src/adapters/http/order_routes.py
  - services/api/tests/test_order_lifecycle.py
- critérios de aceite:
  - Waiter can open/resume an order for a table.
  - Confirmed items can be added through explicit confirmed flow only.
  - Order item statuses can be updated by authorized station users.
  - Closed orders reject new items unless reopened by an approved flow.
- comandos de validação:
  - `cd services/api && pytest tests/test_order_lifecycle.py`
  - `cd services/api && pytest`
- dependências: T-006
- status: pending

### T-008 - Realtime WebSocket backend

- ID: T-008
- objetivo: Add authenticated WebSocket delivery for confirmed kitchen/bar items and status updates.
- arquivos esperados:
  - services/api/src/application/realtime/
  - services/api/src/adapters/websocket/
  - services/api/tests/test_realtime.py
- critérios de aceite:
  - WebSocket requires authentication.
  - Events are scoped by restaurant and station.
  - Only confirmed items emit kitchen/bar events.
  - Reconnect/idempotency behavior is documented and tested at MVP level.
- comandos de validação:
  - `cd services/api && pytest tests/test_realtime.py`
  - `cd services/api && pytest`
- dependências: T-007
- status: pending

### T-009 - Flutter Android waiter app bootstrap

- ID: T-009
- objetivo: Create Flutter Android waiter app with login shell, table list shell and authenticated navigation.
- arquivos esperados:
  - apps/waiter_app/pubspec.yaml
  - apps/waiter_app/lib/main.dart
  - apps/waiter_app/lib/features/auth/
  - apps/waiter_app/lib/features/tables/
  - apps/waiter_app/test/
- critérios de aceite:
  - App launches to login.
  - Successful mocked/API login navigates to table list.
  - Architecture supports API client injection.
- comandos de validação:
  - `cd apps/waiter_app && flutter test`
  - `cd apps/waiter_app && flutter analyze`
- dependências: T-005
- status: pending

### T-010 - Flutter Web console bootstrap

- ID: T-010
- objetivo: Create Flutter Web console for admin, kitchen and bar routes.
- arquivos esperados:
  - apps/web_console/pubspec.yaml
  - apps/web_console/lib/main.dart
  - apps/web_console/lib/features/admin/
  - apps/web_console/lib/features/stations/
  - apps/web_console/test/
- critérios de aceite:
  - Web app has authenticated route structure.
  - Admin route placeholders match planned CRUD.
  - Kitchen/bar route placeholders are station-specific.
- comandos de validação:
  - `cd apps/web_console && flutter test`
  - `cd apps/web_console && flutter analyze`
  - `cd apps/web_console && flutter build web`
- dependências: T-005
- status: pending

### T-011 - Admin web CRUD screens

- ID: T-011
- objetivo: Implement web screens for users, tables, products and open orders.
- arquivos esperados:
  - apps/web_console/lib/features/admin/users/
  - apps/web_console/lib/features/admin/tables/
  - apps/web_console/lib/features/admin/products/
  - apps/web_console/lib/features/admin/orders/
- critérios de aceite:
  - Admin can manage users, tables and products through API.
  - Open orders are visible.
  - Forms validate required fields.
- comandos de validação:
  - `cd apps/web_console && flutter test`
  - `cd apps/web_console && flutter analyze`
- dependências: T-006, T-010
- status: pending

### T-012 - Waiter table/order app flow

- ID: T-012
- objetivo: Implement waiter table selection, order open/resume, history and close-order UI.
- arquivos esperados:
  - apps/waiter_app/lib/features/orders/
  - apps/waiter_app/test/features/orders/
- critérios de aceite:
  - Waiter can open/resume an order for a table.
  - Waiter can view table history.
  - Waiter can request close order.
- comandos de validação:
  - `cd apps/waiter_app && flutter test`
  - `cd apps/waiter_app && flutter analyze`
- dependências: T-007, T-009
- status: pending

### T-013 - Voice recording UX and upload endpoint

- ID: T-013
- objetivo: Add microphone recording flow in the waiter app and backend endpoint to receive voice commands as draft inputs.
- arquivos esperados:
  - apps/waiter_app/lib/features/voice/
  - services/api/src/application/voice/
  - services/api/src/adapters/http/voice_routes.py
  - services/api/tests/test_voice_upload.py
- critérios de aceite:
  - Waiter explicitly starts/stops recording.
  - App handles permission denial and upload failure.
  - Backend stores/handles audio according to documented retention assumptions.
  - Endpoint returns a draft workflow response, not a submitted order.
- comandos de validação:
  - `cd apps/waiter_app && flutter test`
  - `cd services/api && pytest tests/test_voice_upload.py`
- dependências: T-012
- status: pending

### T-014 - Speech-to-text adapter

- ID: T-014
- objetivo: Implement STT interface with mock/demo adapter and provider-ready boundary.
- arquivos esperados:
  - services/api/src/application/voice/stt_port.py
  - services/api/src/adapters/stt/mock_stt.py
  - services/api/tests/test_stt_adapter.py
- critérios de aceite:
  - STT adapter returns transcript and metadata.
  - Failures are explicit and do not submit orders.
  - Provider selection remains swappable.
- comandos de validação:
  - `cd services/api && pytest tests/test_stt_adapter.py`
  - `cd services/api && pytest`
- dependências: T-013
- status: pending

### T-015 - AI order parser adapter

- ID: T-015
- objetivo: Implement parser interface and fixture-backed parser for Portuguese restaurant voice commands.
- arquivos esperados:
  - services/api/src/application/voice/parser_port.py
  - services/api/src/adapters/parser/
  - services/api/tests/fixtures/voice_commands/
  - services/api/tests/test_order_parser.py
- critérios de aceite:
  - Parser maps transcript to draft structured command.
  - Product/table matching uses restaurant context.
  - Ambiguous or low-confidence results require review.
  - Add/change/remove/cancel/close intents are represented.
- comandos de validação:
  - `cd services/api && pytest tests/test_order_parser.py`
  - `cd services/api && pytest`
- dependências: T-014, T-006
- status: pending

### T-016 - Mandatory confirmation backend gate

- ID: T-016
- objetivo: Implement confirmed-draft submission endpoint and guarantee drafts cannot reach kitchen/bar directly.
- arquivos esperados:
  - services/api/src/application/orders/confirm_draft.py
  - services/api/src/adapters/http/confirmation_routes.py
  - services/api/tests/test_confirmation_gate.py
- critérios de aceite:
  - Drafts are persisted/tracked separately from submitted order items.
  - Only explicit confirm action creates submitted order items.
  - Direct draft-to-realtime emission is impossible in tests.
- comandos de validação:
  - `cd services/api && pytest tests/test_confirmation_gate.py`
  - `cd services/api && pytest tests/test_realtime.py`
- dependências: T-015, T-008
- status: pending

### T-017 - Waiter confirmation screen

- ID: T-017
- objetivo: Implement waiter review/edit/reject/confirm screen for parsed voice drafts.
- arquivos esperados:
  - apps/waiter_app/lib/features/confirmation/
  - apps/waiter_app/test/features/confirmation/
- critérios de aceite:
  - Parsed items are displayed before submission.
  - Waiter can edit quantities/items/modifiers.
  - Waiter can reject draft.
  - Confirm button is the only path to backend submission.
- comandos de validação:
  - `cd apps/waiter_app && flutter test test/features/confirmation`
  - `cd apps/waiter_app && flutter analyze`
- dependências: T-016
- status: pending

### T-018 - Kitchen/bar realtime screens

- ID: T-018
- objetivo: Implement kitchen and bar screens that receive confirmed routed items and update status.
- arquivos esperados:
  - apps/web_console/lib/features/stations/kitchen/
  - apps/web_console/lib/features/stations/bar/
  - apps/web_console/test/features/stations/
- critérios de aceite:
  - Kitchen sees only kitchen-routed confirmed items.
  - Bar sees only bar-routed confirmed items.
  - Status updates propagate back through API/WebSocket.
  - Reconnect state is visible.
- comandos de validação:
  - `cd apps/web_console && flutter test test/features/stations`
  - `cd apps/web_console && flutter analyze`
- dependências: T-008, T-010
- status: pending

### T-019 - Demo seed data

- ID: T-019
- objetivo: Add idempotent demo seed data for local end-to-end validation.
- arquivos esperados:
  - infra/seed/
  - services/api/src/infrastructure/seed/
  - docs/demo-flow.md
- critérios de aceite:
  - Seed creates demo restaurant, admin, waiter, kitchen/bar users, tables and products.
  - Seed is idempotent.
  - Demo credentials are documented only for local development.
- comandos de validação:
  - `cd services/api && pytest tests/test_seed.py`
  - `docker compose -f infra/docker-compose.yml up -d postgres`
  - `cd services/api && python -m src.infrastructure.seed.demo`
- dependências: T-006
- status: pending

### T-020 - Full Docker Compose integration

- ID: T-020
- objetivo: Run backend and PostgreSQL together locally with documented environment configuration.
- arquivos esperados:
  - infra/docker-compose.yml
  - services/api/Dockerfile
  - services/api/.dockerignore
  - README.md
- critérios de aceite:
  - Compose starts PostgreSQL and API.
  - API health check passes from host.
  - Migrations and seed can run in local flow.
- comandos de validação:
  - `docker compose -f infra/docker-compose.yml config`
  - `docker compose -f infra/docker-compose.yml up --build`
  - `curl http://localhost:8000/health`
- dependências: T-004, T-019
- status: pending

### T-021 - Automated test suite consolidation

- ID: T-021
- objetivo: Consolidate backend, Flutter, parser, realtime and migration validation commands for CI/local use.
- arquivos esperados:
  - VALIDATION.md
  - README.md
  - scripts/validate.sh
- critérios de aceite:
  - One documented command runs available automated checks.
  - Validation includes confirmation-gate tests.
  - Environment limitations are documented clearly.
- comandos de validação:
  - `bash scripts/validate.sh`
- dependências: T-017, T-018, T-020
- status: pending

### T-022 - Final end-to-end MVP validation

- ID: T-022
- objetivo: Validate the complete flow from voice command to human confirmation to kitchen/bar realtime receipt.
- arquivos esperados:
  - docs/demo-flow.md
  - VALIDATION.md
  - BUGS.md
  - LESSONS_LEARNED.md
- critérios de aceite:
  - Demo flow documents exact steps and expected results.
  - Known limitations/bugs are registered.
  - Human confirmation gate is verified in the final flow.
  - MVP readiness review is recorded.
- comandos de validação:
  - `bash scripts/validate.sh`
  - Manual: login waiter, select table, record command, review draft, confirm, observe kitchen/bar realtime item, update status, close order.
- dependências: T-021
- status: pending
