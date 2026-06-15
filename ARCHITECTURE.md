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

## Backend responsibility glossary

The repository path `services/api` means a deployable backend service/process. It does not mean that business rules should be implemented in generic service classes. Inside the API codebase, names and dependencies must preserve these boundaries:

- **Domain entity/value object**: business concepts and invariants that do not depend on FastAPI, databases, WebSocket clients, AI providers or frameworks.
- **Use case**: one application action that coordinates domain objects and ports, such as `CreateVoiceDraft`, `ConfirmDraftOrder` or `OpenOrder`. A use case owns workflow orchestration and transaction intent, but not HTTP parsing, SQL details or provider SDK calls.
- **Port/interface**: dependency contract required by a use case, such as `OrderRepository`, `SpeechToTextPort`, `OrderParserPort` or `RealtimeEventPublisher`.
- **Gateway/adapter**: infrastructure implementation of a port or external boundary, such as a FastAPI route/controller, WebSocket gateway, PostgreSQL repository, STT provider adapter or parser adapter. Gateways translate protocols and call use cases; they must not own domain decisions.
- **Infrastructure**: technical wiring, settings, database sessions, security primitives, provider clients and framework configuration. Infrastructure composes adapters and use cases but must not bypass use cases for business behavior.

Forbidden coupling:

- FastAPI routes/controllers must not contain order-confirmation business rules; they validate transport input and invoke use cases.
- Repositories must not decide whether a draft can be submitted; they persist and query data requested through ports.
- STT/parser adapters must not create submitted order items or publish kitchen/bar events; they only return draft outputs to use cases.
- WebSocket gateways must not emit AI drafts as station orders; they publish only events produced after explicit confirmation use cases.
- Use cases must depend on ports/interfaces, not concrete PostgreSQL, WebSocket, FastAPI or provider SDK implementations.

## Backend boundaries

- Domain:
  - Restaurant, User, Table, Product, Order, OrderItem, VoiceCommand, ParsedOrderCommand, KitchenTicket.
  - Owns business invariants, including that parsed voice output remains a draft until confirmed.
- Application:
  - Contains use cases and ports/interfaces.
  - Use cases: authenticate user, manage restaurant setup, manage tables/products/users, open/close order, create voice draft, confirm draft order, route confirmed items to kitchen/bar and update order item status.
  - Ports/interfaces: repositories, STT, parser, transaction boundary and realtime publisher contracts consumed by use cases.
- Adapters/gateways:
  - FastAPI REST controllers.
  - FastAPI WebSocket gateway.
  - PostgreSQL repositories.
  - STT provider adapter.
  - Parser provider/rules adapter.
  - Demo/mock adapters.
  - Translate external protocols/provider APIs into application calls without owning domain rules.
- Infrastructure:
  - Database/session setup, settings, auth primitives, dependency injection/composition and external clients.
  - Wires concrete adapters to application ports without bypassing use cases.

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

All tenant-owned tables must include restaurant scoping and indexes for common queries. The T-004 base schema uses Alembic migrations with composite tenant-scoped foreign keys on order/table/user/product relationships to prevent cross-restaurant references at the database boundary.

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
