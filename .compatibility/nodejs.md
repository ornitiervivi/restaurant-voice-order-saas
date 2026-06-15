# Node.js compatibility

## Project scope

Node.js is a candidate backend stack for APIs, domain services, WebSocket/realtime delivery and AI/voice integration adapters.

## Required checks before implementation

- Confirm current LTS Node.js version and package manager.
- Confirm TypeScript, framework, validation library and test runner choices.
- Confirm PostgreSQL driver, migration tooling and transaction handling.
- Confirm WebSocket library/framework support and authentication integration.
- Confirm runtime, build, lint and deployment constraints.

## Constraints

- Node.js services must not submit AI-parsed orders directly; order submission requires explicit human confirmation.
- AI/STT provider integration must be isolated behind interfaces/adapters.
- Java/Spring remains in the repository template only and must not govern this project if Node.js is selected.
