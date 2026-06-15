# Python FastAPI compatibility

## Project scope

Python FastAPI is a candidate backend stack for APIs, domain use cases, WebSocket endpoints and AI/voice integration adapters.

## Required checks before implementation

- Confirm Python stable version, FastAPI version and ASGI server choice.
- Confirm async database driver and migration tooling compatibility with PostgreSQL.
- Confirm validation approach for request/response DTOs and parsed voice command payloads.
- Confirm packaging, dependency management, test runner and lint/static analysis tools.
- Confirm WebSocket support, authentication middleware and deployment runtime constraints.

## Constraints

- FastAPI must not submit AI-parsed orders directly; order submission requires explicit human confirmation.
- AI/STT provider integration must be isolated behind interfaces/adapters.
- Java/Spring remains in the repository template only and must not govern this project if FastAPI is selected.
