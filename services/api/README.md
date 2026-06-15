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
