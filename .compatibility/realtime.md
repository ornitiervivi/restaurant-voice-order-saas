# Realtime compatibility

## Project scope

Realtime governs live delivery of confirmed orders and status updates between backend, waiter app and kitchen/bar screens.

## Required checks before implementation

- Confirm WebSocket or equivalent realtime transport and selected backend framework support.
- Confirm authentication, authorization and tenant isolation for realtime channels.
- Confirm reconnection behavior, message ordering, idempotency and duplicate handling.
- Confirm scaling strategy, pub/sub requirements and deployment platform constraints.
- Confirm browser/mobile client compatibility and fallback behavior.

## Constraints

- Only human-confirmed orders may be emitted to kitchen/bar realtime screens.
- Realtime events must be scoped to the correct restaurant/tenant and destination screen.
- Status updates must be auditable and must not hide delivery failures.
