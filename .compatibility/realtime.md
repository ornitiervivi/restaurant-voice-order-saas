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


## T-008 realtime MVP compatibility

- FastAPI WebSocket is the selected MVP transport for station screens.
- WebSocket access is authenticated with the same signed access token used by HTTP APIs, supplied as the MVP query parameter `token` during WebSocket connection.
- Authorization is tenant-scoped and station-scoped: kitchen users can subscribe only to kitchen events, bar users only to bar events, and admins can subscribe to either station for their restaurant.
- Event delivery is process-local through an in-memory hub for T-008. Clients may reconnect with `last_event_id` to replay missed events retained in the current process for the same restaurant/station.
- Multi-process deployment, durable delivery, and cross-instance idempotency require a future persistent outbox or external pub/sub adapter before production scaling.
