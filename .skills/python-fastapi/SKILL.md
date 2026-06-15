# Python FastAPI Skill

## When to use

Use this skill when the task involves a Python backend, FastAPI APIs, ASGI services, async use cases, validation, PostgreSQL integration, WebSocket endpoints, AI/voice adapters or tests.

## Required reading

- AGENTS.md
- PROJECT_CONTEXT.md
- SPEC.md
- ARCHITECTURE.md
- VALIDATION.md
- `.compatibility/python-fastapi.md`
- `.compatibility/database.md`
- `.compatibility/realtime.md`

## Rules

- Do not implement backend code before asking blocking questions about backend stack selection, API contracts, auth and persistence.
- Plan before changing files.
- Isolate domain/application logic from infrastructure adapters.
- Never persist or emit AI-parsed orders as submitted without explicit human confirmation.
- Register stack decisions and compatibility findings in SDD documents.
- Prefer tests for domain rules, validation and confirmation gates.

## Output

State assumptions, blocking questions, changed files, validation executed and documentation updates.
