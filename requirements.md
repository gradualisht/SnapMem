# SnapMem Development Requirements

This document specifies the development environment requirements for contributing to SnapMem. These rules are mandatory and are in place to ensure stability, reproducibility, and a consistent experience for all contributors.

## 1. Python Version

The choice of Python version is conservative by design, prioritizing long-term stability over access to the latest language features.

-   **Required:** Python 3.11.x
-   **Compatible:** Python 3.12.x

Development must target Python 3.11 to ensure maximum compatibility and stability. While the code is expected to be compatible with Python 3.12, all testing and validation will be performed against the 3.11 runtime.

-   **Unsupported Versions:** Newer feature-development versions of Python (e.g., 3.13, 3.14, and beyond) are **intentionally not supported**.

**Rationale:**
-   **Stability:** We rely on a stable Python runtime. Using a slightly older, mature version avoids bugs and regressions often found in newer releases.
-   **Tooling Support:** Linters, formatters, and other critical development tools have the most reliable support for established Python versions.
-   **Reproducibility:** A fixed version helps guarantee that the application behaves identically across different developer machines.
-   **Contributor Experience:** It is easier for contributors to set up a widely available and well-documented Python version than a bleeding-edge one.

## 2. Environment Management
All development must be performed within an isolated local virtual environment.

-   **Mandatory Virtual Environment:** A virtual environment, created in a `.venv` directory at the project root, is required. This isolates project dependencies from the system and other projects.
-   **No System-Wide Installations:** Project dependencies **MUST NOT** be installed into the system's global Python environment.
-   **No Global Python Modifications:** The project should not require any modifications to the user's global Python installation or system PATH.

## 3. Dependency Philosophy

The project follows a strict, minimalist approach to dependencies to enhance security, reduce maintenance overhead, and align with the Core-First architecture.

-   **Core Engine:** The core processing engine (`/core`) **MUST ONLY** use the Python standard library. No external dependencies are permitted in the core. This is a strict architectural rule.
-   **Interface Layers:** External dependencies are only permitted in interface layers (e.g., the `/cli` package for argument parsing).
-   **Justification:** Every external dependency added to an interface layer must have a clear and explicit justification. We prefer the standard library unless a dependency provides a significant, undeniable benefit.

## 4. Installation Overview

The high-level process for setting up a development environment is as follows:

1.  **Install Python:** Python 3.11 must be installed on the host system, preferably via a standard system package manager (e.g., `apt`, `brew`, `dnf`, or the official installer from python.org).
2.  **Create Virtual Environment:** A local virtual environment must be created within the project's root directory.
3.  **Install Dependencies:** All project dependencies must be installed exclusively into this virtual environment.

This process ensures that the project setup is self-contained and does not interfere with the host system.

## 5. Explicit Non-Requirements

To clarify the scope and maintain a simple setup, the following are **not required** for SnapMem development:

-   **No Docker:** The application is designed to run directly on the host OS without containerization.
-   **No Cloud SDKs:** As an offline-only tool, no cloud-specific libraries (e.g., `boto3`, `azure-sdk`) are needed.
-   **No Global Python Tools:** The project does not require the installation of global command-line tools via `pip` or other package managers.
-   **No Experimental Builds:** Development must use official, stable releases of Python. Nightly, beta, or release-candidate builds are not permitted.