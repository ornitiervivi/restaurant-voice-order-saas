# API Contracts

Shared API contract artifacts for clients and backend.

## Current state

This directory is intentionally a skeleton for TASK T-001. No generated schemas or clients are committed yet.

## Intended responsibilities

- Store OpenAPI exports or generated clients when contract generation is introduced.
- Keep mobile and web clients aligned with backend request/response schemas.
- Document compatibility-breaking contract changes.

## Contract safety

Order draft contracts must model `requires_confirmation` explicitly so AI/STT/parser output cannot be confused with submitted order items.
