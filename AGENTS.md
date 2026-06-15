# AGENTS.md

## Mandatory operating rules

Before any non-trivial change, read the relevant SDD/harness files:

1. PROJECT_CONTEXT.md
2. SPEC.md
3. ARCHITECTURE.md
4. DECISIONS.md
5. TASKS.md
6. PLAN.md
7. AI_HARNESS.md
8. AGENT_ROLES.md
9. SKILLS.md
10. VALIDATION.md
11. CODE_REVIEW.md
12. TECH_RADAR.md
13. BUGS.md
14. LESSONS_LEARNED.md
15. Applicable `.compatibility/*`
16. Applicable `.skills/*/SKILL.md`

If any required project detail is missing, ask blocking questions before implementation.

## Project rule

This project is a SaaS for restaurant voice ordering. The system must allow waiters to speak orders into an Android app, convert speech into structured order items, show a confirmation screen, and only then send confirmed orders to kitchen/bar screens in real time.

AI must never submit orders directly without human confirmation.

## Workflow

1. Read SDD/harness files.
2. Select roles from AGENT_ROLES.md.
3. Identify blocking questions.
4. Plan before coding.
5. Update project documentation.
6. Implement the smallest safe increment.
7. Run or define validation.
8. Review code.
9. Update TASKS.md, DECISIONS.md, BUGS.md, LESSONS_LEARNED.md when relevant.

## Scope control

Do not expand scope without approval. Do not implement unrelated features. Prefer small, reversible commits. Preserve existing behavior unless the task explicitly changes it.

## Code rules

Write production-oriented code. Prefer clean architecture, SOLID, clean code, expressive names, low coupling, high cohesion, automated tests, explicit validation, secure defaults, and compatibility checks.

Do not leave TODO comments as implementation. Do not hide failures. Record limitations when validation cannot be executed.
