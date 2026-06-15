# PROJECT_CONTEXT.md

## Project name

restaurant-voice-order-saas

## Origin

Workana MVP request for a SaaS system where restaurant waiters create orders through voice commands.

## Objective

Reduce manual typing, order mistakes, communication failures with kitchen/bar, and slow service during peak hours by letting waiters speak orders naturally, reviewing an AI-generated draft, and submitting only after human confirmation.

## Product description

SaaS for restaurants with:

- Android waiter app for voice-first table service.
- Backend API for multi-tenant restaurant operations.
- PostgreSQL persistence for restaurants, users, tables, products, orders, order items and audit data.
- Admin web panel for configuration and open-order monitoring.
- Kitchen/bar realtime screens for confirmed orders and status updates.
- Speech-to-text and AI order parser isolated behind adapters.

## MVP scope

- Android waiter app:
  - Login.
  - Table list.
  - Open and close orders/tabs.
  - Voice recording.
  - AI/STT draft generation.
  - Mandatory confirmation/edit screen before submission.
  - Table order history.
- AI flow:
  - Speech-to-text for Brazilian Portuguese voice commands.
  - Parser for table, quantities, products, modifiers, additions, alterations, cancellations and close-account intent.
  - Ambiguity/low-confidence flags that force review.
- Admin panel:
  - Restaurant setup.
  - User/waiter management.
  - Table management.
  - Product/menu management.
  - Open order visualization.
- Kitchen/bar screen:
  - Realtime receipt of human-confirmed items.
  - Item status updates.
- Local development:
  - Monorepo.
  - Docker Compose with PostgreSQL and backend.
  - Demo seed data.
  - Automated validation commands.

## Non-goals for initial MVP

- Direct AI submission to kitchen/bar without human confirmation.
- Payment processing.
- Fiscal invoice integration.
- Inventory management.
- Multi-branch enterprise reporting.
- Offline-first synchronization beyond basic network failure UX.
- Production deployment automation beyond documented Docker/local validation.

## Critical rule

AI must never submit an order without waiter confirmation. AI/STT/parser output is always a draft until an authenticated human waiter explicitly confirms it.

## Blocking questions

No blocking questions remain for planning because the Workana description and repository harness provide enough information to create an executable MVP plan. Provider-specific and UI-detail questions are deferred to the relevant implementation tasks before coding.

## Planning assumptions

- Primary language and market are Brazilian Portuguese restaurants.
- MVP backend will use Python FastAPI after technical evaluation in DECISIONS.md.
- Web admin and kitchen/bar screens will use Flutter Web to share UI skills and model contracts with the Android app unless a future decision changes this.
- Authentication will start with email/password plus JWT access/refresh tokens and role-based authorization.
- PostgreSQL is the source of truth.
- Realtime delivery uses authenticated WebSocket channels scoped by restaurant and station type.
- STT provider is initially abstracted; local/demo parser fixtures and a mock STT adapter are acceptable before paid provider selection.
- Demo data will include at least one restaurant, one admin, one waiter, tables, products and example orders.

## Initial repository status

The repository currently contains SDD/harness documentation and planning artifacts. Implementation code is intentionally deferred until the stack/question gate is satisfied by specific follow-up tasks.

## Last meaningful update

2026-06-15: Completed T-008 realtime WebSocket backend for authenticated station delivery of confirmed order item and status-update events with tenant/station scoping and MVP replay by event id.
