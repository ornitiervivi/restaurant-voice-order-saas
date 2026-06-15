# TECH_RADAR.md

## Purpose

Track technologies, versions, compatibility decisions and known incompatibilities for the Workana restaurant voice ordering MVP.

## Active project candidates

| Area | Candidate | Status | Notes |
|---|---|---|---|
| Mobile | Flutter | Candidate | Android waiter app |
| Web | Flutter Web | Candidate | Admin and kitchen/bar screens if confirmed |
| Web | Equivalent frontend | Candidate | Alternative for admin/kitchen/bar if Flutter Web is rejected |
| Backend | Python FastAPI | Candidate | Strong for API and AI integration |
| Backend | Node.js | Candidate | Alternative backend stack with TypeScript APIs |
| Database | PostgreSQL | Candidate | Relational order data and tenant isolation |
| Realtime | WebSocket | Candidate | Kitchen/bar updates and waiter status sync |
| AI voice | STT plus order parser | Candidate | Voice-to-draft structured order flow |

## Template-only technologies

| Area | Candidate | Status | Notes |
|---|---|---|---|
| Backend | Java/Spring | Template only | Must not govern this project if FastAPI or Node.js is selected |

## Decision rules

- Record chosen backend stack in DECISIONS.md before backend implementation.
- Record Flutter Web versus equivalent frontend decision before web implementation.
- Record AI/STT provider and parser constraints before AI voice implementation.
- Record realtime transport constraints before kitchen/bar realtime implementation.
