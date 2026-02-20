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

## Code Readability & Learning Guidelines

- Prefer simple, explicit code over clever or compressed solutions.
- Variable and function names must clearly express intent.
- Comments should explain *why* a decision was made, not repeat *what* the code does.
- Public functions and core modules must include docstrings describing purpose, inputs, and outputs.
- Inline comments are allowed only for non-obvious logic or constraints.
- If code requires a long explanatory comment, it likely needs refactoring.

### Learning-Oriented Design

- Code structure should be easy to follow for a junior developer.
- Complex ideas should be broken into small, well-named functions.
- Avoid introducing abstractions until they are justified by repeated need.

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

## Branching & Integration Rules

- All development happens in feature branches.
- Feature branches are always created from `develop`.
- Completed features are merged into `develop` via pull request.
- `main` only receives tested, release-ready code via merges from `develop`.
- AI agents must never commit directly to `main`.

### Dependency Order

- Features must respect architectural dependency order.
- Core engine work must be completed and merged before CLI work.
- CLI work must be completed and merged before GUI work.
- No feature may depend on unfinished branches.
- If a feature requires unmerged work, it must wait — not reimplement.

---

## Python Environment Rules

- The project uses a local Python virtual environment located at `.venv/`.
- All development, execution, and dependency installation MUST occur inside this virtual environment.
- System-wide Python installations MUST NOT be modified.
- Global package installation (`pip install` without an active .venv) is forbidden.
- The Python interpreter used by tools, scripts, and editors must always resolve to `.venv/bin/python`.
- If the virtual environment is not active, the correct action is to STOP and activate it — not to install globally.

### Tooling Expectations

- VS Code is expected to automatically detect and use the `.venv` interpreter.
- Any AI agent (including Copilot) must assume that a virtual environment is active.
- If the virtual environment is not active, the correct action is to STOP and activate it before proceeding.

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

---

## Documentation & Status Workflow

The following rules are firm project policy:

- The project distinguishes between internal status notes and official documentation.
- Internal progress, decisions, and open questions may be recorded in `/docs/status/`.
- Status notes are informal, chronological, and may be incomplete.
- Official documentation (README.md and files in /docs/) MUST NOT be modified automatically.

### Documentation Updates

- Documentation updates must be explicit and intentional.
- An AI agent MUST NOT update README.md or official docs unless explicitly instructed.
- When significant changes are made, the agent may suggest documentation updates,
  but must not apply them without confirmation.

### Final Documentation Consolidation

- Before a release or major milestone, status notes may be used to propose
  documentation updates.
- The agent may assist in consolidating documentation, but the final decision
  always belongs to the supervisor.
