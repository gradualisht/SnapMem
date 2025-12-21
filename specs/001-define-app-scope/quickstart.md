# Quickstart: SnapMem CLI

**Purpose**: Provide a simple guide for using the final command-line application.
**Plan**: [plan.md](plan.md)

This guide describes how a user will interact with the SnapMem CLI once it is built.

## Installation

SnapMem will be packaged as a standard Python application.

```bash
pip install snapmem
```

## Usage

The primary command takes the path to your Snapchat `memories_history.json` file and an output directory.

### Basic Command

```bash
snapmem process --input /path/to/your/memories_history.json --output /path/to/save/organized_memories
```

### Arguments

-   `--input`: **(Required)** The path to the `memories_history.json` file from your Snapchat export.
-   `--output`: **(Required)** The path to an **empty** directory where you want the organized media to be saved. If the directory does not exist, SnapMem will create it. If it is not empty, SnapMem will stop and show an error.

### Example

1.  **Download and unzip your Snapchat data.**
    You will have a folder, let's say `snapchat-export`, that contains `memories_history.json` and a `memories` subfolder.

2.  **Create an empty directory for the output.**
    ```bash
    mkdir my-organized-memories
    ```

3.  **Run the command.**
    The `--input` path points to the JSON file, and you must also tell SnapMem where the root of the export is with `--source`.

    ```bash
    snapmem process \
      --input ~/Downloads/snapchat-export/json/memories_history.json \
      --output ./my-organized-memories \
      --source ~/Downloads/snapchat-export/
    ```
    *(Note: The exact path to `memories_history.json` can vary inside the export, so the user must provide it).*

## Expected Output

After running, you will see a summary in your terminal:

```
Processing complete.

- Total items found: 1500
- Successfully organized: 1495
- Failed to organize: 5

Failures:
- memories/media123.jpg (Reason: Source file not found)
- memories/media456.mp4 (Reason: Invalid date in JSON record)
...

Your organized memories are available at: ./my-organized-memories
```

Inside the `my-organized-memories` directory, you will find your media sorted into folders by year and month:

```
my-organized-memories/
├── 2024/
│   ├── 11/
│   │   ├── 2024-11-15_image.jpg
│   │   └── 2024-11-20_video.mp4
│   └── 12/
│       └── 2024-12-05_image.jpg
└── 2025/
    └── 01/
        └── 2025-01-01_image.jpg
```
