# AGENTS.md — SnapMem

This file defines the rules and constraints for all AI-assisted development
(GitHub Copilot, ChatGPT, other LLMs).

All generated code MUST follow these rules.

---

## Project Context

SnapMem is an open-source, privacy-first, offline-only tool that extracts and
organizes Snapchat Memories from the official Snapchat JSON export.

This project is NOT a one-off script.
It is designed as a maintainable software product with a clear architecture.

---

## Core Principles (Non-Negotiable)

- Offline-only processing (no uploads, no servers)
- Privacy-first (no telemetry, no analytics, no tracking)
- Core-first architecture
- Deterministic and reproducible output
- Clear separation of concerns
- Tool-quality code, not tutorial code

If a generated solution violates any of these, it is WRONG.

---

## Architecture Rules

### Core Engine
- All business logic lives in `/core`
- Core MUST NOT:
  - import CLI code
  - import GUI code
  - print to stdout
  - depend on UI frameworks
- Core functions must return data or raise typed errors

### CLI
- CLI code lives in `/cli`
- CLI is a thin adapter:
  - parse arguments
  - call core
  - display progress and results
- CLI MUST NOT reimplement core logic

### GUI (future)
- GUI must call the same core engine as the CLI
- No duplicated business logic is allowed

---

## Code Style & Quality

- Avoid global state
- Prefer pure functions where possible
- Use explicit data models instead of loose dicts
- Use meaningful names over short names
- No "magic values" without explanation
- Code must be readable without comments explaining basic logic

---

## Error Handling Rules

- The application MUST NOT abort entirely due to individual item failures
- Errors must be:
  - collected
  - categorized
  - returned as part of a summary report
- Silent failures are NOT allowed
- Exceptions must be explicit and meaningful

---

## Testing Rules

- Core logic SHOULD be testable without file system side effects
- Parsing, naming, and date handling MUST be test-covered
- Tests should live in `/tests`
- Tests must not rely on real Snapchat data
- Use sanitized fixtures only

---

## Determinism & Reproducibility

- Running SnapMem twice on the same input MUST produce the same output
- File naming must be deterministic
- Ordering must be explicit, not accidental

---

## Dependency Rules

- Avoid unnecessary dependencies
- Prefer standard library when reasonable
- Do NOT introduce heavy frameworks into the core
- Dependencies must have a clear justification

---

## AI Usage Rules

- AI may assist with:
  - boilerplate
  - refactoring
  - test scaffolding
- AI must NOT:
  - invent features
  - expand scope
  - bypass architectural rules
- If uncertain, AI should ask for clarification instead of guessing

---

## Scope Control

Explicitly OUT OF SCOPE unless stated otherwise:
- Cloud processing
- Web upload services
- Snapchat API integration
- User accounts or authentication
- Monetization features

---

## Review Checklist (Before Committing)

Before committing AI-generated code, ensure:
- Core logic is UI-independent
- No privacy violations exist
- Errors are handled and reported
- Code matches the project constitution
- Changes do not introduce scope creep
