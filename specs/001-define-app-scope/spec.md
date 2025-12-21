# Feature Specification: Define SnapMem Application Scope

**Feature Branch**: `001-define-app-scope`  
**Created**: 2025-12-20  
**Status**: Draft  
**Input**: User description: "Specify the functional scope of an application called "SnapMem"."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Technical User Processes Memories via CLI (Priority: P1)

A user comfortable with the command line wants to process their downloaded Snapchat data export. They need a reliable way to extract all their memories without manually sorting through technical files.

**Why this priority**: This is the core value proposition and serves the initial user persona. It establishes the fundamental processing logic that a future GUI will also use.

**Independent Test**: Can be fully tested by running the command-line tool with a valid export file and an output directory. The test passes if the media is organized correctly and a summary report is generated.

**Acceptance Scenarios**:

1. **Given** a user has a valid Snapchat export folder, **When** they run the application from the command line, providing the path to the `memories_history.json` file and an output directory, **Then** the application processes the files and creates organized media folders in the specified output location.
2. **Given** the processing is complete, **When** the user checks the console, **Then** a summary report is displayed, showing counts of successful and failed items.

---

### User Story 2 - Non-Technical User Processes Memories via GUI (Priority: P2)

A non-technical user wants to easily organize their Snapchat Memories without using a command line. They need a simple, visual tool to achieve the same outcome.

**Why this priority**: This expands the user base significantly by providing an accessible interface. It is P2 because it depends on the core logic developed for the CLI.

**Independent Test**: Can be tested by opening the desktop application, selecting an input file and output directory through the UI, and running the process. The test passes if the output is identical to the CLI output for the same input.

**Acceptance Scenarios**:

1. **Given** a user has the desktop application open, **When** they use the file picker to select their `memories_history.json` and an output folder, and click "Start", **Then** the application begins processing and displays a progress indicator.
2. **Given** the processing is complete, **When** the user views the application window, **Then** a summary report is displayed visually.

---

### Edge Cases

- **Invalid Input**: What happens when the user provides a path to a file that is not a valid Snapchat JSON export? The system should report a clear error and exit gracefully.
- **Missing Media**: How does the system handle a JSON entry that points to a media file that is missing from the export? It should log the failure for that specific item and continue processing others, including it in the final failure count.
- **Existing Output**: What happens if the output directory already contains files? The system MUST stop and report a clear error, requiring the user to provide an empty or non-existent directory path.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a path to a Snapchat `memories_history.json` file as its primary input.
- **FR-002**: System MUST parse the input JSON file to extract all memory records and their associated media file references.
- **FR-003**: System MUST copy the identified media files from their source location within the export to a user-specified output directory. It MUST NOT modify or move the original files.
- **FR-004**: System MUST organize the copied media into a human-readable folder structure based on the date of the memory (e.g., `YYYY/MM`).
- **FR-005**: System MUST generate and present a summary report upon completion, detailing the number of media files successfully processed and the number of failures.
- **FR-006**: System MUST operate entirely on the local machine. No part of the core processing may require or use a network connection.

### Key Entities *(include if feature involves data)*

- **Snapchat Export**: The user-provided folder containing the `memories_history.json` file and associated subfolders of media (photos and videos).
- **Memory Record**: A single JSON object within the main export file that represents one memory, containing a timestamp and a path to the associated media file.
- **Organized Media File**: The resulting image or video file after being copied by the application into the structured output directory.
- **Summary Report**: A data object produced at the end of a run, containing statistics like `files_processed`, `files_succeeded`, and `files_failed`, along with a list of specific failures.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a valid Snapchat export, 100% of media files referenced in the JSON are correctly copied and organized into the output directory.
- **SC-002**: The application can process an export containing 10,000 media items in under 5 minutes on a standard consumer laptop (e.g., 4-core CPU, 8GB RAM).
- **SC-003**: The final output folder structure is organized chronologically by year and month, making it easily browsable for a non-technical user.
- **SC-004**: The summary report accurately reflects the exact number of items processed, copied, and any items that failed, ensuring the user has a clear accounting of the result.
- **SC-005**: Application monitoring confirms zero network requests are initiated during the entire processing lifecycle.

## Explicit Exclusions (Out of Scope)
- Cloud processing or any form of data upload.
- Direct integration with any social media APIs, including Snapchat's.
- Features for editing, viewing, or modifying media content.
- User accounts, authentication, or cross-device syncing.
