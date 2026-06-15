# AI Voice Order Parser Skill

## When to use

Use this skill when the task involves audio capture, speech-to-text, natural language parsing, structured order commands, ambiguity handling, confidence scoring or waiter confirmation for voice orders.

## Required reading

- AGENTS.md
- PROJECT_CONTEXT.md
- SPEC.md
- ARCHITECTURE.md
- VALIDATION.md
- `.compatibility/ai-voice.md`

## Rules

- Do not implement AI/STT integration before asking blocking questions about provider, language, privacy, latency, cost and failure handling.
- Plan before changing files.
- Treat parser output as a draft command until a human waiter confirms it.
- Never send, persist as submitted or emit AI-parsed orders directly to kitchen/bar.
- Force review for ambiguous, invalid or low-confidence commands.
- Register provider decisions, known failures and lessons when relevant.

## Output

State assumptions, blocking questions, changed files, validation executed and documentation updates.
