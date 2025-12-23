# SnapMem Architecture

This document outlines the software architecture of SnapMem. It is intended for contributors and reviewers who need to understand the project's structure, design principles, and data flow.

The architecture is designed to be robust, maintainable, and privacy-preserving, adhering to the rules defined in the project's constitution.

## 1. High-Level Overview

SnapMem uses a **Core-First** (or "Hexagonal") architecture. This design isolates the application's primary business logic from its user interfaces and external services.

The central component is the **Core Engine**, a self-contained library that performs all data processing. This engine is consumed by one or more **Adapters**—in this case, a Command-Line Interface (CLI) and a future Graphical User Interface (GUI).

This strict separation ensures that the core logic remains independent of how users interact with it.

### Architecture Diagram

```ascii
+-----------------+      +----------------------+
|   Input Files   |      |   User Interface     |
| (JSON, media)   |      | (CLI or future GUI)  |
+-------+---------+      +----------+-----------+
        |                            |
        | 1. Provide Paths           | 2. Invoke Core Engine
        |                            | with paths & options
        v                            v
+----------------------------------------------------+
|                   Core Engine (`/core`)              |
|                                                    |
|  - Parse `memories_history.json`                   |
|  - Resolve media file paths                        |
|  - Generate deterministic output file structure    |
|  - Copy files to output directory                  |
|  - Collect errors and generate a summary report    |
|                                                    |
+------------------------+---------------------------+
                         | 3. Return structured result
                         | (data object, not text)
                         v
+------------------------+---------------------------+
|           Output Data & Report                     |
| (Organized Files & Summary Report)                 |
+----------------------------------------------------+
```

## 2. Rationale for Core-First Design

The Core-First design was chosen for several critical reasons:

-   **Maintainability:** Business logic is centralized, preventing duplication and making the system easier to understand and modify.
-   **Testability:** The core engine can be tested in isolation, without needing to simulate user input or interact with the file system directly for many tests.
-   **Flexibility:** New local adapters (like a desktop GUI) can be added to provide different ways of interacting with the application without changing the core logic.
-   **Privacy & Security:** By strictly defining the core's boundaries, we can enforce critical rules, such as prohibiting network access, which is fundamental to our privacy guarantees.

## 3. Component Responsibilities

### a. Core Engine (`/core`)

The Core Engine contains all the business logic for the application. It is a pure data processing component.

**Responsibilities:**
-   Parsing the Snapchat `memories_history.json` file.
-   Validating the input data model.
-   Resolving the location of media files based on the JSON data.
-   Generating a deterministic and reproducible file naming and directory structure.
-   Executing the file operations to copy media to the organized output directory.
-   Collecting all processing errors into a structured report.

**Prohibitions (Non-Negotiable Rules):**
The Core Engine **MUST NOT**:
-   Import any code from the `cli/` or `gui/` packages.
-   Print directly to the console (`stdout`/`stderr`).
-   Contain any code for network communication (e.g., HTTP requests).
-   Depend on any UI-specific frameworks or libraries.
-   Make any assumptions about the user interface.

All functions in the core must either return structured data or raise typed, specific errors.

### b. Command-Line Interface (`/cli`)

The CLI is a thin adapter that provides a command-line front-end for the Core Engine.

**Responsibilities:**
-   Parsing command-line arguments (e.g., input path, output path).
-   Performing basic input validation (e.g., checking if paths exist).
-   Invoking the Core Engine with the appropriate parameters.
-   Receiving the structured result object from the core.
-   Displaying progress, results, and the final error report to the user in the terminal.

The CLI **MUST NOT** reimplement any business logic found in the core.

### c. GUI (Future)

A future desktop GUI will be another thin adapter, functionally equivalent to the CLI.

**Responsibilities:**
-   Providing a graphical way for users to select input and output directories.
-   Calling the **exact same Core Engine** as the CLI.
-   Displaying progress and results in a user-friendly graphical format.

The GUI **MUST NOT** contain any duplicated business logic.

## 4. Data Flow

1.  The user, via an interface (CLI/GUI), provides the path to the Snapchat export and a desired output directory.
2.  The interface calls the main entry point of the Core Engine, passing these paths as arguments.
3.  The Core Engine reads and parses `memories_history.json`.
4.  For each memory, it resolves the media file, determines its new name and path, and copies it to the output directory.
5.  Throughout this process, any failures (e.g., a missing media file) are caught and added to an error collection.
6.  After processing all memories, the Core Engine constructs a final summary report object, which includes statistics and the list of errors.
7.  This report object is returned to the calling interface (CLI/GUI).
8.  The interface formats and displays the information from the report object to the user.

## 5. Error Handling Strategy

SnapMem is designed to be resilient. A failure on a single item should not terminate the entire process.

-   **Error Collection:** The Core Engine does not crash on recoverable errors. Instead, it logs the error internally (with context, like the media item that failed) and continues processing other items.
-   **Categorization:** Errors are categorized (e.g., `FileNotFound`, `InvalidJsonData`) to provide clear, actionable feedback.
-   **Summary Report:** The final report returned by the core includes a complete list of all errors that occurred. This allows the user to see exactly which files could not be processed and why. Silent failures are not permitted.

## 6. Determinism and Reproducibility

A key architectural guarantee is that running SnapMem twice on the same input data will produce an identical output.

-   **Deterministic Naming:** File and folder names are generated based on fixed rules and data from the input (e.g., media creation date), not random or system-dependent values.
-   **Explicit Ordering:** Where order matters, it is explicitly defined (e.g., sorting by date), not left to filesystem or language-specific quirks.

This ensures that the output is predictable and verifiable.

## 7. Extensibility

This architecture is designed for future extension without requiring a major refactor. Because the core is UI-agnostic, we can:
-   Develop the GUI without impacting the CLI or the core logic.
-   Potentially add other interfaces (e.g., a library/plugin for another application) that consume the core.
-   Update the core logic (e.g., to support a new version of the Snapchat export format) in one place, and all interfaces will benefit immediately.
