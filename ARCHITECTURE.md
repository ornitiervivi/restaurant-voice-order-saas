# ARCHITECTURE.md

## Target architecture

Clean Architecture with explicit separation between domain, application use cases, adapters and infrastructure. The product is a monorepo containing backend, mobile/web clients, shared contracts, infrastructure and documentation.

## Final MVP stack decision

- Android app: Flutter.
- Web admin/kitchen/bar: Flutter Web for MVP.
- Backend: Python FastAPI.
- Database: PostgreSQL.
- Migrations: Alembic or equivalent Python migration tooling.
- Realtime: FastAPI WebSocket endpoints backed by an internal event service for MVP; external pub/sub can be introduced later if scaling requires it.
- AI/voice: speech-to-text and parser adapters behind application interfaces.
- Local environment: Docker Compose.

## Why Python FastAPI over Node.js for this MVP

FastAPI is selected because the MVP has AI/STT/parser integration needs, strong request validation requirements and WebSocket support. Python reduces integration friction for ML/NLP libraries and AI SDKs while still providing high-performance async APIs. Node.js remains a viable alternative, but it adds less advantage for the AI-heavy parts of this product and would still require strict TypeScript discipline to match FastAPI/Pydantic validation ergonomics.

## Proposed monorepo structure

```text
/
  apps/
    waiter_app/              # Flutter Android app
    web_console/             # Flutter Web admin + kitchen/bar screens
  services/
    api/                     # Python FastAPI backend
      src/
        domain/              # Entities, value objects, domain rules
        application/         # Use cases and ports/interfaces
        adapters/            # HTTP, persistence, STT, parser, realtime adapters
        infrastructure/      # DB, settings, auth, external clients
        tests/
      migrations/            # PostgreSQL migrations
  packages/
    api_contracts/           # Shared OpenAPI/schema/generated client artifacts if needed
    ui_shared/               # Optional shared Flutter widgets/design tokens
  infra/
    docker-compose.yml
    postgres/
    seed/
  docs/
    demo-flow.md
  .compatibility/
  .skills/
  PROJECT_CONTEXT.md
  SPEC.md
  ARCHITECTURE.md
  DECISIONS.md
  PLAN.md
  TASKS.md
```

## Backend boundaries

- Domain:
  - Restaurant, User, Table, Product, Order, OrderItem, VoiceCommand, ParsedOrderCommand, KitchenTicket.
- Application:
  - Authenticate user.
  - Manage restaurant setup.
  - Manage tables/products/users.
  - Open/close order.
  - Create voice draft.
  - Confirm draft order.
  - Route confirmed items to kitchen/bar.
  - Update order item status.
- Adapters:
  - FastAPI REST controllers.
  - FastAPI WebSocket gateway.
  - PostgreSQL repositories.
  - STT provider adapter.
  - Parser provider/rules adapter.
  - Demo/mock adapters.

## Database model outline

- restaurants
- users
- tables
- products
- product_modifiers or product_options
- orders
- order_items
- voice_commands
- parsed_order_drafts
- kitchen_tickets or station_events
- audit_events

All tenant-owned tables must include restaurant scoping and indexes for common queries.

## Realtime design

- Authenticated WebSocket connection after login.
- Channels scoped by restaurant and role/station:
  - restaurant:{id}:waiter:{user_id}
  - restaurant:{id}:kitchen
  - restaurant:{id}:bar
  - restaurant:{id}:admin
- Events:
  - confirmed_order_item_created
  - order_item_status_changed
  - order_closed
  - table_order_changed
- Only confirmed items generate kitchen/bar events.

## AI/voice design

- Flutter records audio and submits it to backend.
- Backend stores only the minimum necessary metadata for MVP unless retention is explicitly approved.
- STT adapter returns transcript plus confidence/metadata where available.
- Parser adapter maps transcript to a draft command using current restaurant products/tables.
- Draft response includes ambiguity flags and requires_confirmation=true.
- Confirm endpoint accepts edited/approved structured items and creates submitted order items.

## Security design

- JWT-based auth for MVP with password hashing and refresh-token strategy.
- Role-based access controls.
- Tenant isolation in every repository and WebSocket channel.
- Secrets via environment variables.
- No sensitive audio/text logs by default.

## Validation architecture

- Backend unit tests for domain/use cases.
- Backend integration tests for REST, WebSocket and database migrations.
- Flutter widget/client tests for confirmation gate and core navigation.
- Parser fixture tests for Portuguese command examples and ambiguity cases.
- Docker Compose smoke test for API + PostgreSQL.
- Manual end-to-end demo checklist.
