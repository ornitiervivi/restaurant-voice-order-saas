# Infrastructure

Local development infrastructure for the restaurant voice ordering SaaS.

## Current state

This directory is intentionally a skeleton for TASK T-001. Docker Compose and PostgreSQL assets are added in later tasks.

## Intended responsibilities

- Local Docker Compose environment.
- PostgreSQL service configuration for development.
- Seed data and demo environment support.
- Operational documentation for local validation.

## Safety notes

- Do not commit real secrets.
- Demo credentials must be local-development only.
- Realtime and database services must preserve tenant isolation.
