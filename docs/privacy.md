# SnapMem Privacy Policy

**Effective Date:** December 23, 2025

This document explains how SnapMem handles your data. We believe in privacy by design, and our commitment to protecting your information is reflected in our architecture, not just our words.

This is a technical document, not a marketing promise. It describes the verifiable constraints placed on the software.

## 1. Core Principle: Offline-Only

SnapMem is an **offline-only** tool. This is not just a feature; it is the foundation of the entire application.

- **No Network Code:** The core processing engine of SnapMem contains no code for network communication. It cannot make network requests, connect to APIs, or transmit any data over the internet.
- **Architectural Enforcement:** The application is architecturally designed to prevent network access in its core components. The business logic is entirely separated from any potential UI or future component that *could* have network access, ensuring the data processing itself remains offline.

## 2. What SnapMem Does With Your Data

SnapMem's data handling is limited to the explicit task it is designed for: organizing your Snapchat Memories export.

1.  **Read-Only Access to Input:** You provide the path to your Snapchat `memories_history.json` file and associated media files. SnapMem reads this data to perform its function. **Your original files are never modified, moved, or deleted.**
2.  **Local Processing:** All processing occurs on your local machine. Data is not sent to any server, cloud service, or third-party application.
3.  **Writing the Organized Output:** You provide an output directory. SnapMem writes the newly organized media files and metadata to this location. The application's file system access is restricted to this designated output path for write operations.

The application's entire function is to transform data from the input path to the output path, with no steps in between that could expose your data.

## 3. What SnapMem Explicitly Does NOT Do

To be perfectly clear, SnapMem **never** performs any of the following actions:

- **No Uploads:** Your data is never uploaded to any remote server, cloud storage provider, or web service.
- **No Telemetry or Analytics:** The application does not collect any usage data, performance metrics, or analytics. We do not know who you are, how you use the tool, or what data you process.
- **No Tracking:** There are no tracking pixels, cookies, or user identification mechanisms.
- **No Third-Party APIs:** SnapMem does not integrate with the Snapchat API or any other web-based API. It is a passive tool that only reads the files you provide.
- **No User Accounts:** The application does not require or support user accounts, logins, or authentication.

## 4. Filesystem Access

SnapMem's access to your filesystem is limited and user-directed:

- **Input Path (Read-Only):** The application requires you to specify the location of your Snapchat export. It will only read from this directory and its subdirectories.
- **Output Path (Write):** The application requires you to specify a destination for the organized output. It will only write to this directory.
- **No Scanning:** SnapMem does not scan your hard drive or access files outside of the explicitly provided input and output paths.

## 5. Data Sovereignty and Guarantees

"Data sovereignty" means you have complete control over your own data. SnapMem is designed to uphold this principle.

- **Your Data Never Leaves Your Machine:** This is the most critical guarantee. Because the tool is offline-only, you can be certain that your private memories remain on your hardware.
- **Verifiable and Deterministic:** Running SnapMem on the same input will always produce the exact same output. There are no hidden variables or external factors influencing the result.
- **Open Source:** While this document aims to be clear, the ultimate guarantee is the source code itself. The project is open-source, allowing for independent audit and verification of all claims made here.

By building SnapMem on a foundation of offline-only processing and architectural separation of concerns, we ensure that your privacy is not a policy that can change, but a technical reality of the software itself.
