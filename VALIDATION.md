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
