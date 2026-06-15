# PLAN.md

## Planning gate

### Blocking questions

No blocking questions remain for this documentation-only planning increment. The Workana description is sufficient to select a technical MVP direction and create sequential tasks.

### Assumptions used

- MVP market/language: Brazilian Portuguese.
- Backend: Python FastAPI.
- Mobile/web: Flutter Android + Flutter Web.
- Database: PostgreSQL.
- Realtime: authenticated WebSocket.
- AI/STT/parser providers remain adapter-based until provider-specific implementation tasks.
- AI outputs are drafts and always require human confirmation.

## Roles selected

- Product Analyst
- Solution Architect
- Backend Engineer
- Frontend/Mobile Engineer
- Database Engineer
- AI/Voice Engineer
- Security Reviewer
- DevOps Engineer
- QA/Test Engineer
- Code Reviewer
- SDD Scribe

## Execution strategy

Implement the product in small, reversible increments. Each increment must update documentation when decisions change, include validation commands, and preserve the mandatory confirmation gate.

## Increment plan

### Phase 0 - Planning and decision baseline

Goal: establish scope, selected stack, monorepo shape, validation path and task backlog.

Deliverables:

- Updated PROJECT_CONTEXT.md, SPEC.md, ARCHITECTURE.md, DECISIONS.md, PLAN.md and TASKS.md.
- Final backend stack decision: Python FastAPI.
- No implementation code.

Validation:

- `git diff --check`
- Documentation review against AGENTS.md and CODE_REVIEW.md.

### Phase 1 - Monorepo and local foundation

Goal: create repository folders and local tooling without product behavior.

Deliverables:

- `apps/waiter_app/`
- `apps/web_console/`
- `services/api/`
- `infra/docker-compose.yml`
- root README and environment examples.

Validation:

- Formatting/static text checks.
- Docker Compose config validation.

### Phase 2 - Backend base

Goal: bootstrap FastAPI with health checks, settings, test framework and clean architecture folders.

Deliverables:

- FastAPI service skeleton.
- Health endpoint.
- Config loading.
- Test runner.
- CI-ready commands.

Validation:

- Backend unit tests.
- API health check.

### Phase 3 - PostgreSQL and migrations

Goal: connect backend to PostgreSQL and create first migrations.

Deliverables:

- Database connection.
- Migration tooling.
- Tables for restaurants, users, tables, products, orders and order items.
- Tenant indexes and constraints.

Validation:

- Migration up/down.
- Repository smoke tests.

### Phase 4 - Authentication and authorization

Goal: secure API and role access.

Deliverables:

- Password hashing.
- Login endpoint.
- JWT access/refresh flow.
- Role and restaurant scoping guards.

Validation:

- Auth unit/integration tests.
- Negative authorization tests.

### Phase 5 - Admin setup CRUD

Goal: manage core restaurant data.

Deliverables:

- Restaurant profile endpoints.
- Users CRUD.
- Tables CRUD.
- Products CRUD including station routing.

Validation:

- CRUD API tests.
- Tenant isolation tests.

### Phase 6 - Order lifecycle backend

Goal: support open orders/tabs and confirmed order item management.

Deliverables:

- Open/resume order.
- Add confirmed items.
- Change item status.
- Close order.
- Table history.

Validation:

- Domain/use-case tests.
- Confirmation gate tests.

### Phase 7 - Realtime backend

Goal: deliver confirmed items and status changes live.

Deliverables:

- Authenticated WebSocket gateway.
- Restaurant/station channels.
- Event schema.
- Reconnect/idempotency strategy.

Validation:

- WebSocket integration tests.
- Confirmed-only emission tests.

### Phase 8 - Flutter Android waiter app foundation

Goal: create basic waiter app shell.

Deliverables:

- Flutter project.
- Login screen.
- Authenticated navigation.
- Table list.
- Order history shell.

Validation:

- Flutter tests.
- Android build/debug smoke check when environment supports it.

### Phase 9 - Flutter Web console foundation

Goal: create admin and station web shell.

Deliverables:

- Flutter Web project/shell.
- Admin CRUD screens.
- Kitchen/bar routes.
- Authenticated navigation.

Validation:

- Flutter web tests/build.
- Browser smoke check when environment supports it.

### Phase 10 - Voice recording workflow

Goal: capture waiter audio and submit to backend as a draft workflow.

Deliverables:

- Microphone permission UX.
- Record/stop states.
- Audio upload API endpoint.
- Draft response model.

Validation:

- Flutter recording UX tests where possible.
- Backend audio endpoint tests.

### Phase 11 - Speech-to-text adapter

Goal: convert audio to transcript behind an interface.

Deliverables:

- STT port/interface.
- Mock/demo STT adapter.
- Provider-ready adapter boundary.
- Privacy/retention docs.

Validation:

- STT fixture tests.
- Failure-mode tests.

### Phase 12 - AI parser adapter

Goal: transform transcript into structured draft order commands.

Deliverables:

- Parser schema.
- Product/table matching rules.
- Ambiguity/confidence flags.
- Add/change/remove/cancel/close intent handling.

Validation:

- Portuguese parser fixture tests.
- Ambiguity tests.

### Phase 13 - Mandatory human confirmation UX

Goal: ensure waiter review/edit is the only path to submission.

Deliverables:

- Confirmation screen.
- Edit/reject actions.
- Confirm endpoint integration.
- Error handling for ambiguous drafts.

Validation:

- UI tests for no-submit-before-confirm.
- Backend tests rejecting draft direct submission.

### Phase 14 - Kitchen/bar realtime screens

Goal: display confirmed routed items and status updates.

Deliverables:

- Kitchen view.
- Bar view.
- Status update controls.
- Realtime reconnect feedback.

Validation:

- WebSocket UI/client tests.
- Manual two-client smoke test.

### Phase 15 - Docker Compose and demo data

Goal: run the MVP locally with realistic seed data.

Deliverables:

- Compose services.
- Seed script.
- Demo accounts, restaurant, tables and products.
- Demo flow docs.

Validation:

- Compose up.
- Seed idempotency test.
- Demo checklist.

### Phase 16 - Final end-to-end validation

Goal: validate the complete Workana demo flow.

Deliverables:

- Automated regression suite.
- Manual E2E script.
- Known limitations.
- MVP readiness review.

Validation:

- Backend tests.
- Flutter tests/builds.
- Migration checks.
- Docker Compose smoke.
- Manual voice-to-confirmed-kitchen flow.
