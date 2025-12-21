# Data Model: SnapMem

**Purpose**: Define the core data structures for the application.
**Plan**: [plan.md](plan.md)
**Source**: Entities identified in [spec.md](spec.md)

## Core Entities

### 1. `Memory`

Represents a single Snapchat Memory item extracted from the export. This is the primary data object passed through the processing pipeline.

-   **Fields**:
    -   `date` (datetime): The timestamp of when the memory was created. Used for sorting and organizing.
    -   `media_type` (Enum: `IMAGE`, `VIDEO`): The type of media associated with the memory.
    -   `source_path` (Path): The absolute path to the original media file within the Snapchat export directory.
    -   `relative_path` (str): The relative path of the media file as it appears in the JSON export (e.g., `memories/123.jpg`).

-   **Validation Rules**:
    -   `date` must be a valid datetime object.
    -   `source_path` must exist and be a file.

### 2. `MediaFile`

Represents a media file that has been successfully processed and is ready for export.

-   **Fields**:
    -   `source_path` (Path): The absolute path to the original media file.
    -   `destination_path` (Path): The target absolute path where the file will be copied, including the new deterministic filename.

-   **State Transitions**:
    -   A `Memory` object is transformed into a `MediaFile` object after it has been successfully validated and its destination path has been determined.

### 3. `FailedItem`

Represents a memory that could not be processed. This allows for robust error collection without halting the entire application.

-   **Fields**:
    -   `memory` (Memory): The original `Memory` object that failed.
    -   `error` (str): A human-readable message explaining the reason for the failure (e.g., "Source file not found", "Invalid date format").

### 4. `Report`

A summary of the entire processing run. This is the final output of the core engine, which can then be displayed by the CLI or GUI.

-   **Fields**:
    -   `total_processed` (int): The total number of memory records found in the JSON file.
    -   `succeeded_count` (int): The number of media files successfully copied.
    -   `failed_count` (int): The number of media files that failed to process.
    -   `failures` (List[`FailedItem`]): A list of all items that failed, along with the reason.
    -   `output_location` (Path): The root directory where the organized media was saved.

-   **Validation Rules**:
    -   `total_processed` must equal `succeeded_count` + `failed_count`.
