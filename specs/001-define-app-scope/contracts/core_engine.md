# API Contract: SnapMem Core Engine

**Purpose**: Define the public interface of the `core` engine.
**Plan**: [plan.md](plan.md)

This document specifies the contract that the `core` engine provides to any user-facing adapter (e.g., `cli`, `gui`). Adherence to this contract ensures that the business logic remains decoupled and reusable.

## Main Entry Point

### `process_export(input_path: Path, output_path: Path, source_dir: Path) -> Report`

This is the sole entry point for executing the full data processing pipeline.

-   **Parameters**:
    -   `input_path` (Path): The absolute path to the `memories_history.json` file.
    -   `output_path` (Path): The absolute path to the target directory for the organized media. This directory MUST be empty or non-existent.
    -   `source_dir` (Path): The absolute path to the user-provided, read-only root of the unzipped Snapchat export directory. The engine is restricted to this directory when resolving media files.

-   **Returns**:
    -   A `Report` object (see [data-model.md](data-model.md)) summarizing the results of the operation.

-   **Behavior**:
    -   The function orchestrates the entire workflow: parsing, resolving, exporting, and reporting.
    -   **It MUST guarantee deterministic output**: Given the same `input_path`, `output_path`, and `source_dir` content, the resulting file and folder structure in `output_path` will be identical every time.
    -   It MUST NOT `print` to standard output or raise exceptions for individual file-processing errors.
    -   All partial failures (e.g., a missing media file) will be collected and included in the returned `Report`.
    -   It will only raise an exception for critical, unrecoverable errors, such as:
        -   `InputFileNotFoundError`: If `input_path` does not exist.
        -   `OutputDirectoryNotEmptyError`: If `output_path` exists and is not empty.
        -   `InvalidExportError`: If the input JSON is malformed.

## Data Flow (Internal)

The `process_export` function will internally follow this data flow, with each step being a distinct, testable component:

1.  **Parse**:
    -   **Input**: `input_path`
    -   **Output**: `List[Memory]`
    -   **Action**: Reads the JSON file and transforms each entry into a `Memory` object.

2.  **Resolve & Export**:
    -   **Input**: `List[Memory]`, `output_path`, `source_dir`
    -   **Output**: `(List[MediaFile], List[FailedItem])`
    -   **Action**: Iterates through each `Memory` object. For each one, it attempts to locate the source media file and determine its destination path. If successful, it creates a `MediaFile` object. If it fails, it creates a `FailedItem` object. It then copies the files.

3.  **Report**:
    -   **Input**: The results from the previous steps.
    -   **Output**: `Report`
    -   **Action**: Compiles the statistics and failure details into the final `Report` object.
