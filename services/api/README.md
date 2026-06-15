# API Service

Python FastAPI backend planned for the restaurant voice ordering SaaS.

## Current state

This directory is intentionally a skeleton for TASK T-001. No FastAPI application code has been added yet.

## Intended responsibilities

- Authentication, authorization, roles and tenant isolation.
- Restaurant, user, table and product management APIs.
- Order lifecycle and human-confirmed order item persistence.
- Voice draft workflow behind STT and parser interfaces/adapters.
- Authenticated WebSocket delivery for kitchen/bar/admin/waiter updates.

## Stack boundary

- Selected backend stack: Python FastAPI.
- Database: PostgreSQL with migrations in a later task.
- AI/STT/parser providers must remain isolated behind application ports.
- AI drafts must not be submitted or emitted to realtime channels without explicit waiter confirmation.


## Responsibility boundaries

The directory name `services/api` identifies the backend deployable service. It must not be interpreted as permission to place all business logic in generic service classes.

Planned implementation boundaries:

- `domain/`: entities, value objects and framework-independent invariants.
- `application/`: use cases plus ports/interfaces. Use cases orchestrate workflows and depend only on ports.
- `adapters/`: gateways and adapters for HTTP, WebSocket, PostgreSQL, STT and parser integrations. They translate external protocols into use-case calls.
- `infrastructure/`: settings, database sessions, auth primitives, dependency wiring and provider clients.

Separation rules:

- A route/controller may call a use case, but must not implement the use case.
- A gateway/adapter may implement a port, but must not contain domain decisions.
- A repository may persist/query data, but must not decide confirmation eligibility.
- The confirmation gate belongs in domain/application rules and must be covered by tests before realtime emission is introduced.
