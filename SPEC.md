# SPEC.md

## Product goal

Enable restaurant waiters to register orders by voice in an Android app, convert speech into structured draft order actions, require human confirmation, and then deliver confirmed items to kitchen/bar screens in real time.

## Actors

- Restaurant admin: configures restaurant data, users, tables and products.
- Waiter: manages table service from the Android app.
- Kitchen/bar operator: receives confirmed items and updates preparation status.
- AI/STT services: produce draft transcription and parsing outputs only.

## Main waiter flow

1. Waiter logs in.
2. Waiter views tables for the restaurant.
3. Waiter selects a table and opens or resumes an order/tab.
4. Waiter presses a microphone button and speaks naturally.
5. System records audio and sends it to the backend voice workflow.
6. Backend transcribes audio through a speech-to-text adapter.
7. Backend parses transcript into a draft structured command through an AI/parser adapter.
8. Waiter reviews interpreted items/actions on a confirmation screen.
9. Waiter edits or rejects invalid/ambiguous items as needed.
10. Waiter confirms the final draft.
11. Backend persists confirmed order items and emits realtime kitchen/bar events.
12. Kitchen/bar operators update item status.
13. Waiter views table history and closes the order when appropriate.

## Example voice command

Input: "Mesa 12, duas picanhas ao ponto, uma Coca Zero e uma água sem gás."

Expected draft structured output before confirmation:

- table: 12
- action: add_items
- items:
  - name: Picanha
    quantity: 2
    modifiers: ao ponto
  - name: Coca Zero
    quantity: 1
  - name: Água sem gás
    quantity: 1
- confidence: present per parsed field where supported
- requires_confirmation: true

## Supported voice actions for MVP

- Add item.
- Change item quantity.
- Remove item.
- Cancel item.
- Close table/order request.

## Functional requirements

### Authentication and authorization

- Users authenticate before accessing app or web panels.
- Roles: admin, waiter, kitchen, bar.
- Users are scoped to a restaurant/tenant.
- API and WebSocket access require authorization.

### Restaurant setup

- Admin can create/update restaurant profile data in MVP setup flow.
- Admin can manage users, tables and products.
- Products include name, station routing target (kitchen/bar), availability and optional modifiers.

### Order lifecycle

- A table can have an open order/tab.
- Waiters can open, view and close orders.
- Confirmed items are persisted with status and audit metadata.
- Item status changes are visible to waiter and admin.

### Voice workflow

- Audio capture begins only after waiter action.
- Audio/STT/parser outputs are drafts.
- Ambiguous, invalid or low-confidence output must be shown for review/edit.
- No draft may be emitted to kitchen/bar before waiter confirmation.

### Realtime workflow

- Kitchen/bar screens receive only confirmed items routed to their station.
- Status updates are propagated to waiter/admin screens.
- Events are scoped to the correct restaurant.
- Duplicate/reconnect behavior must be validated before relying on realtime delivery.

## Non-functional requirements

- Clean Architecture boundaries between domain, application, adapters and infrastructure.
- Secure defaults for auth, secrets and tenant isolation.
- Automated tests for critical domain rules and confirmation gate.
- Docker Compose local environment.
- Demo seed data for end-to-end validation.
- Explicit provider isolation for STT/parser.

## Acceptance criteria

- No AI-parsed order is submitted before human confirmation.
- Invalid or ambiguous parsing requires user review/edit.
- Kitchen/bar screen receives confirmed orders in real time.
- Admin can manage users, tables and products.
- Waiter can complete the full path from login to table history and close order.
- Validation commands exist for backend, frontend/mobile, migrations, realtime and final demo flow.
