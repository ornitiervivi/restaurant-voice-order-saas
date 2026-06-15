# Realtime WebSocket Skill

## When to use

Use this skill when the task involves WebSocket, live kitchen/bar updates, event delivery, reconnection, channel authorization, realtime scaling or order status propagation.

## Required reading

- AGENTS.md
- PROJECT_CONTEXT.md
- SPEC.md
- ARCHITECTURE.md
- VALIDATION.md
- `.compatibility/realtime.md`

## Rules

- Do not implement realtime code before asking blocking questions about transport, auth, tenant isolation, ordering and scaling.
- Plan before changing files.
- Emit only human-confirmed orders to kitchen/bar screens.
- Ensure reconnect/idempotency behavior is defined before relying on realtime delivery.
- Register compatibility constraints and validation evidence.

## Output

State assumptions, blocking questions, changed files, validation executed and documentation updates.
