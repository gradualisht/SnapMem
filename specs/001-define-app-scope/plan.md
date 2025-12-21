# Implementation Plan: SnapMem Core and CLI

**Branch**: `001-define-app-scope` | **Date**: 2025-12-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/home/dev/code/dev/products/SnapMem/specs/001-define-app-scope/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the technical approach for building SnapMem, a privacy-first, offline-only tool to process Snapchat Memories exports. The architecture is designed around a shared core engine and a thin CLI adapter, ensuring maintainability and future extensibility for a GUI. The primary goal is to deliver a robust command-line tool that reliably organizes media files and provides clear user feedback, while adhering strictly to the project constitution.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- Core: None (Standard Library only)
- CLI: Implementation detail, choice of `Typer` or `argparse` does not affect architecture.
- Testing: `pytest`
**Storage**: Filesystem (user-specified input/output directories)
**Testing**: `pytest` for unit and integration tests.
**Target Platform**: Cross-platform (Windows, macOS, Linux).
**Project Type**: Single project (Core library + CLI entry point).
**Performance Goals**: Process 10,000 media items in under 5 minutes on a standard consumer laptop.
**Constraints**: Must be fully functional offline. Must not write to any location outside the specified output directory.
**Scale/Scope**: Initial version supports a single user processing a local data export.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Privacy & Data Sovereignty**: **Ok**. The design is entirely local. No data leaves the user's machine.
- **II. Offline-First Behavior**: **Ok**. No network access is required or implemented.
- **III. Core-First Architecture**: **Ok**. The design explicitly separates the `core` engine from the `cli` adapter.
- **IV. Separation of Concerns**: **Ok**. The data flow is broken into distinct `parse`, `resolve`, `export`, and `report` stages.
- **V. Determinism & Reproducibility**: **Ok**. The file organization logic will be based on sortable, explicit data (date from memory), not filesystem order.
- **VI. Code Quality & Maintainability**: **Ok**. The plan uses clear data models and avoids global state.
- **VII. User Experience & Transparency**: **Ok**. The CLI will provide progress and a final summary report. Errors are collected, not thrown.
- **VIII. Explicit Non-Goals**: **Ok**. The scope is limited to local processing and avoids all listed non-goals.

## Project Structure

### Documentation (this feature)

```text
specs/001-define-app-scope/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
# Option 1: Single project (DEFAULT)
core/
├── __init__.py
├── models.py      # Data structures (e.g., Memory, Report)
├── parse.py       # Logic for reading and validating the JSON export
├── resolve.py     # Logic for finding media files
├── export.py      # Logic for copying and organizing files
├── report.py      # Logic for generating the summary report
└── errors.py      # Custom, typed exceptions

cli/
├── __init__.py
└── main.py        # CLI argument parsing and calls to the core engine

tests/
├── fixtures/      # Sample (sanitized) data for testing
├── test_parse.py
├── test_resolve.py
└── test_export.py
```

**Structure Decision**: The existing single project structure is a perfect fit for this application. It correctly isolates the `core` business logic from the `cli` presentation layer, which aligns with the constitution's Core-First principle. This structure will allow a future `gui` module to be added at the same level as `cli`, reusing the `core` engine without modification.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None*    | *N/A*      | *N/A*                               |
