# CODE_REVIEW.md

## Review checklist

- Change matches requested scope.
- Architecture boundaries preserved.
- No unrelated refactor.
- No hidden behavior change.
- Naming is expressive.
- Error handling is explicit.
- Security concerns reviewed.
- Tests cover relevant cases.
- Compatibility checked.
- SDD files updated.

## Workana stack review gates

- Flutter changes respect Android waiter app and optional Flutter Web constraints.
- Backend changes are consistent with the selected Python FastAPI or Node.js decision.
- Java/Spring guidance is treated as template-only unless explicitly selected in DECISIONS.md.
- PostgreSQL decisions cover migrations, indexes, transactions and tenant isolation.
- WebSocket/realtime changes cover auth, reconnection, ordering, idempotency and delivery failures.
- AI voice changes keep STT/parser behind interfaces and include confidence/ambiguity handling.
- No AI-generated order can bypass human confirmation before submission or realtime delivery.
- Blocking questions were asked or documented when stack, provider, API, auth or UX details were missing.
- A plan existed before implementation.

## Pull request title standard

All pull request titles for task-based changes must use this exact format:

```text
T-###: Imperative summary
```

Rules:

- Start with the task ID from `TASKS.md`, zero-padded as already written there, followed by a colon and one space.
- Use an imperative, concise English summary after the prefix, for example `T-003: Add local PostgreSQL Docker Compose setup`.
- Do not use alternative formats such as appending `(T-003)` at the end, omitting the task ID, or changing the separator.
- For non-task correction PRs, use `CHORE: Imperative summary` unless the user provides a more specific prefix.
