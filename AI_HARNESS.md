# AI_HARNESS.md

## Purpose

Define how AI agents must work in this repository before product planning or implementation.

## Mandatory behavior

- Read SDD files before work.
- Use AGENT_ROLES.md roles.
- Load only relevant `.skills/*/SKILL.md` files.
- Check applicable `.compatibility/*` files for the selected stack area.
- Ask blocking questions before risky implementation or irreversible decisions.
- Plan before coding.
- Keep documentation alive.
- Register stack decisions, bugs and lessons.
- Validate before delivering when possible.
- Prefer small increments.

## Stack scope

The harness must support the Workana MVP stack candidates:

- Flutter for the Android waiter app.
- Flutter Web or equivalent frontend for admin/kitchen/bar screens.
- Python FastAPI or Node.js for the backend.
- PostgreSQL for persistence.
- WebSocket or equivalent realtime transport for kitchen/bar delivery and status updates.
- AI voice/STT/parser components for converting speech into draft structured orders.

Java/Spring remains in the template only and does not govern this project unless a future explicit decision changes the stack.

## Non-negotiable safety rule

AI-generated or AI-parsed orders are drafts only. They must never be submitted, persisted as submitted or emitted to kitchen/bar screens until a human waiter confirms them.

## Required output for non-trivial work

- Roles used.
- Files read.
- Plan.
- Blocking questions or assumptions.
- Stack/compatibility decision impact.
- Files changed.
- Validation executed.
- Documentation updated.
