from pathlib import Path
from collections import defaultdict

from core.models import Memory, ExportItem, MediaType, WarningRecord, SkippedItem


def build_export_plan(
    memories: list[Memory],
    output_root: Path,
    export_base_path: Path
) -> tuple[list[ExportItem], list[WarningRecord], list[SkippedItem]]:
    
    export_items: list[ExportItem] = []
    warnings: list[WarningRecord] = []
    skipped: list[SkippedItem] = []
    
    destination_tracker: dict[Path, int] = defaultdict(int)
    
    for memory in memories:
        try:
            source_path = _resolve_source_path(memory, export_base_path)
        except ValueError as e:
            skipped.append(SkippedItem(
                item_id=memory.id,
                reason="InvalidSourcePath",
                details=str(e)
            ))
            continue
        
        destination = _compute_destination_path(
            memory=memory,
            output_root=output_root,
            destination_tracker=destination_tracker
        )
        
        export_item = ExportItem(
            memory=memory,
            source_path=source_path,
            destination_path=destination
        )
        export_items.append(export_item)
    
    return export_items, warnings, skipped


def _resolve_source_path(memory: Memory, export_base_path: Path) -> Path:
    
    if not memory.download_url:
        raise ValueError("Memory has no download_url")
    
    url = memory.download_url.replace("\\", "/")
    
    if url.startswith("file://"):
        url = url[7:]
    elif url.startswith("/"):
        url = url[1:]
    
    source_path = export_base_path / url
    return source_path


def _compute_destination_path(
    memory: Memory,
    output_root: Path,
    destination_tracker: dict[Path, int]
) -> Path:
    
    year = memory.timestamp.strftime("%Y")
    month = memory.timestamp.strftime("%m")
    
    folder_path = output_root / year / month
    
    base_filename = memory.suggested_filename
    stem = base_filename.rsplit(".", 1)[0]
    extension = base_filename.rsplit(".", 1)[1] if "." in base_filename else ""
    
    candidate = folder_path / base_filename
    
    if candidate not in destination_tracker:
        destination_tracker[candidate] = 1
        return candidate
    
    counter = destination_tracker[candidate]
    destination_tracker[candidate] += 1
    
    if extension:
        unique_filename = f"{stem}_{counter}.{extension}"
    else:
        unique_filename = f"{stem}_{counter}"
    
    unique_path = folder_path / unique_filename
    destination_tracker[unique_path] = 1
    
    return unique_path
