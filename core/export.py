import shutil
from pathlib import Path

from core.models import ExportItem, ErrorRecord, SuccessRecord, ExportSummary
from core.errors import FileOperationError


def export_items(
    items: list[ExportItem],
    source_dir: Path,
    output_dir: Path
) -> ExportSummary:
    
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()
    
    summary = ExportSummary()
    summary.total_memories_found = len(items)
    
    for item in items:
        try:
            _export_single_item(item, source_dir, output_dir, summary)
        except Exception as e:
            _record_export_failure(item, str(e), summary)
    
    summary.successful_exports = len(summary.successes)
    summary.failed_exports = len(summary.errors)
    
    return summary


def _export_single_item(
    item: ExportItem,
    source_dir: Path,
    output_dir: Path,
    summary: ExportSummary
) -> None:
    
    source_path = item.source_path.resolve()
    destination_path = item.destination_path.resolve()
    
    _validate_path_within_directory(source_path, source_dir, "source")
    _validate_path_within_directory(destination_path, output_dir, "destination")
    
    if not source_path.exists():
        raise FileOperationError(
            f"Source file not found: {source_path.name}",
            context={"path": str(source_path)}
        )
    
    if not source_path.is_file():
        raise FileOperationError(
            f"Source path is not a file: {source_path.name}",
            context={"path": str(source_path)}
        )
    
    if destination_path.exists():
        raise FileOperationError(
            f"Destination already exists: {destination_path.name}",
            context={"path": str(destination_path)}
        )
    
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(source_path, destination_path)
    
    file_size = destination_path.stat().st_size
    
    summary.successes.append(SuccessRecord(
        memory_id=item.memory.id,
        destination_path=destination_path,
        file_size_bytes=file_size
    ))


def _validate_path_within_directory(
    path: Path,
    allowed_dir: Path,
    path_type: str
) -> None:
    
    try:
        path.relative_to(allowed_dir)
    except ValueError:
        raise FileOperationError(
            f"Invalid {path_type} path: outside allowed directory",
            context={
                "path": str(path),
                "allowed_dir": str(allowed_dir)
            }
        )


def _record_export_failure(
    item: ExportItem,
    error_message: str,
    summary: ExportSummary
) -> None:
    
    error_type = "ExportError"
    context = None
    
    if "not found" in error_message.lower():
        error_type = "SourceNotFound"
    elif "already exists" in error_message.lower():
        error_type = "DestinationExists"
    elif "outside allowed" in error_message.lower():
        error_type = "PathValidationError"
    elif "permission" in error_message.lower():
        error_type = "PermissionError"
    
    if hasattr(item.memory, 'source_json_path') and item.memory.source_json_path:
        context = str(item.memory.source_json_path)
    
    summary.errors.append(ErrorRecord(
        item_id=item.memory.id,
        error_type=error_type,
        message=error_message,
        context=context
    ))
