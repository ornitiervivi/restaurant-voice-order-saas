# ARCHITECTURE.md

## Target architecture

Clean Architecture with explicit separation between domain, application, adapters and infrastructure.

## Suggested stack

- Android app: Flutter.
- Web admin/kitchen/bar: Flutter Web or equivalent frontend.
- Backend: Python FastAPI or Node.js after technical decision.
- Database: PostgreSQL.
- Realtime: WebSocket.
- Local environment: Docker Compose.
- AI/voice: isolated service/use case for speech-to-text and command parsing.

## Core domains

- Restaurant
- User
- Table
- Product
- Order
- OrderItem
- VoiceCommand
- ParsedOrderCommand
- KitchenTicket

## Integration boundaries

Voice, AI parsing, realtime delivery and persistence must be isolated behind interfaces.
