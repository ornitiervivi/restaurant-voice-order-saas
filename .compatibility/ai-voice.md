# AI voice compatibility

## Project scope

AI voice covers audio capture handoff, speech-to-text, natural language parsing, ambiguity handling and conversion into structured restaurant order commands.

## Required checks before implementation

- Confirm STT provider, model/version, language support for Brazilian Portuguese and expected latency.
- Track provider limits, costs, privacy constraints, retention policies and known failure modes.
- Confirm parser output schema for table, items, quantities, modifiers, removals, cancellations and close-order actions.
- Define confidence thresholds, ambiguity rules and fallback UX for manual review.
- Validate how audio/text data is stored, redacted, logged or discarded.

## Constraints

- AI voice must never submit orders directly.
- Every parsed order action must be reviewed and confirmed by a human waiter before kitchen/bar delivery.
- Low-confidence, invalid or ambiguous parsing must force review/edit instead of automatic submission.
