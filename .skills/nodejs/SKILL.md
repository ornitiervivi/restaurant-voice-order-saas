# Node.js Skill

## When to use

Use this skill when the task involves a Node.js backend, TypeScript APIs, services, validation, PostgreSQL integration, WebSocket endpoints, AI/voice adapters or tests.

## Required reading

- AGENTS.md
- PROJECT_CONTEXT.md
- SPEC.md
- ARCHITECTURE.md
- VALIDATION.md
- `.compatibility/nodejs.md`
- `.compatibility/database.md`
- `.compatibility/realtime.md`

## Rules

- Do not implement backend code before asking blocking questions about backend stack selection, API contracts, auth and persistence.
- Plan before changing files.
- Keep TypeScript boundaries explicit between domain, application and adapters.
- Never persist or emit AI-parsed orders as submitted without explicit human confirmation.
- Register stack decisions and compatibility findings in SDD documents.
- Prefer tests for domain rules, validation and confirmation gates.

## Output

State assumptions, blocking questions, changed files, validation executed and documentation updates.
