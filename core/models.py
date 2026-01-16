"""Core data models for SnapMem - pure data structures with no IO, network, or UI logic."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class MediaType(Enum):
    """Media content type: image, video, or unknown."""
    
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Memory:
    """A single Snapchat memory with metadata and media file reference."""
    
    id: str
    timestamp: datetime
    media_type: MediaType
    download_url: str
    suggested_filename: str
    original_filename: Optional[str] = None
    duration_seconds: Optional[float] = None
    source_json_path: Optional[Path] = None


@dataclass(frozen=True)
class ExportItem:
    """Links a memory's source file to its destination path for export."""
    
    memory: Memory
    source_path: Path
    destination_path: Path


@dataclass
class ExportPlan:
    """Collection of export operations with target output directory."""
    
    items: list[ExportItem] = field(default_factory=list)
    output_directory: Optional[Path] = None


@dataclass(frozen=True)
class ErrorRecord:
    """Records a processing failure with type, message, and context."""
    
    item_id: str
    error_type: str
    message: str
    context: Optional[str] = None


@dataclass(frozen=True)
class WarningRecord:
    """Records a non-fatal issue that doesn't stop processing."""
    
    item_id: str
    warning_type: str
    message: str


@dataclass(frozen=True)
class SkippedItem:
    """Records an item intentionally excluded from processing."""
    
    item_id: str
    reason: str
    details: Optional[str] = None


@dataclass(frozen=True)
class SuccessRecord:
    """Records a successful export with destination and file size."""
    
    memory_id: str
    destination_path: Path
    file_size_bytes: int


@dataclass
class ExportSummary:
    """Aggregates counts and detailed records from a complete export operation."""
    
    total_memories_found: int = 0
    successful_exports: int = 0
    failed_exports: int = 0
    warnings_count: int = 0
    skipped_count: int = 0
    errors: list[ErrorRecord] = field(default_factory=list)
    warnings: list[WarningRecord] = field(default_factory=list)
    skipped: list[SkippedItem] = field(default_factory=list)
    successes: list[SuccessRecord] = field(default_factory=list)
