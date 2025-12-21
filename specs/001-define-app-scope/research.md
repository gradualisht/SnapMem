# Research: SnapMem Technical Decisions

**Purpose**: Resolve unknowns from the implementation plan before design.
**Plan**: [plan.md](plan.md)

## Research Tasks

1.  **CLI Framework Selection**: Evaluate `Typer` vs. `argparse` for the CLI.
2.  **GUI Framework Selection (Future)**: Initial investigation into cross-platform GUI toolkits suitable for a Python core.

## Decisions

### 1. CLI Framework Selection

-   **Decision**: The choice between `Typer` and `argparse` is a minor implementation detail for the `cli` adapter and does not affect the core architecture. The initial implementation will use `Typer` for its superior developer experience and minimal boilerplate, but this can be changed without impacting the core engine.
-   **Rationale**:
    -   The "thin adapter" principle means the CLI layer should be as simple as possible. `Typer` achieves this more effectively than `argparse`.
    -   Since the core engine is completely decoupled, the CLI framework can be swapped in the future if needed with zero changes to the business logic. This decision is low-risk and easily reversible.
-   **Alternatives Considered**:
    -   `argparse`: Standard library, but requires more boilerplate code.
    -   `Click`: A viable alternative, but `Typer` provides a more modern, type-hint-driven interface.

### 2. GUI Framework Selection (Future)

-   **Decision**: Defer final choice, but `Tauri` or `PySide (Qt)` are leading candidates. This decision does not impact the current CLI-focused work.
-   **Rationale**:
    -   The Core-First architecture ensures that the choice of a future GUI framework has no bearing on the immediate implementation of the core logic and CLI.
    -   `Tauri` (using a Rust backend with a web frontend) is a strong contender for its lightweight, modern, and secure nature. It can call the Python core engine as a sidecar process.
    -   `PySide (Qt)` is a mature option for building native-looking UIs directly in Python.
    -   No further research is needed at this stage, as this choice is out of scope for the current implementation phase.
-   **Alternatives Considered**:
    -   `Tkinter`: Standard library, but dated UI and capabilities.
    -   `Electron`: Powerful, but often results in large application sizes and high memory usage.
