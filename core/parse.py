import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.errors import ParseError
from core.models import Memory, MediaType, WarningRecord


def parse_export(
    json_data: dict[str, Any],
    source_path: Path | None = None
) -> tuple[list[Memory], list[WarningRecord]]:
    
    memories: list[Memory] = []
    warnings: list[WarningRecord] = []
    
    memories_data = _extract_memories_array(json_data)
    
    if memories_data is None:
        warnings.append(WarningRecord(
            item_id=str(source_path) if source_path else "unknown",
            warning_type="NoMemoriesFound",
            message="JSON structure does not contain recognizable memories array"
        ))
        return memories, warnings
    
    for idx, item in enumerate(memories_data):
        item_id = str(idx)
        
        try:
            memory = _parse_memory_item(item, source_path)
            if memory:
                memories.append(memory)
        except Exception as e:
            warnings.append(WarningRecord(
                item_id=item_id,
                warning_type="ParseFailure",
                message=f"Failed to parse memory item: {str(e)}"
            ))
    
    return memories, warnings


def parse_export_file(json_path: Path) -> tuple[list[Memory], list[WarningRecord]]:
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ParseError(
            f"Invalid JSON in {json_path.name}",
            context={"path": str(json_path), "error": str(e)}
        )
    except FileNotFoundError:
        raise ParseError(
            f"File not found: {json_path}",
            context={"path": str(json_path)}
        )
    
    return parse_export(data, json_path)


def _extract_memories_array(data: dict[str, Any]) -> list[dict] | None:
    
    possible_keys = [
        "Saved Media",
        "Memories",
        "memories",
        "saved_media",
        "Media"
    ]
    
    for key in possible_keys:
        if key in data and isinstance(data[key], list):
            return data[key]
    
    if isinstance(data, dict) and len(data) == 1:
        single_value = next(iter(data.values()))
        if isinstance(single_value, list):
            return single_value
    
    return None


def _parse_memory_item(
    item: dict[str, Any],
    source_path: Path | None
) -> Memory | None:
    
    memory_id = _extract_id(item)
    timestamp = _extract_timestamp(item)
    media_type = _extract_media_type(item)
    download_url = _extract_download_url(item)
    
    if not download_url:
        return None
    
    original_filename = item.get("Media Type") or item.get("filename")
    duration = _extract_duration(item)
    
    suggested_filename = _generate_filename(
        timestamp=timestamp,
        media_type=media_type,
        original_filename=original_filename,
        memory_id=memory_id
    )
    
    return Memory(
        id=memory_id,
        timestamp=timestamp,
        media_type=media_type,
        download_url=download_url,
        suggested_filename=suggested_filename,
        original_filename=original_filename,
        duration_seconds=duration,
        source_json_path=source_path
    )


def _extract_id(item: dict[str, Any]) -> str:
    
    for key in ["id", "ID", "memory_id", "Memory ID"]:
        if key in item:
            return str(item[key])
    
    return str(hash(frozenset(item.items())))[:16]


def _extract_timestamp(item: dict[str, Any]) -> datetime:
    
    timestamp_keys = ["Date", "date", "timestamp", "created_at", "Created"]
    
    for key in timestamp_keys:
        if key in item:
            value = item[key]
            
            if isinstance(value, str):
                return _parse_timestamp_string(value)
            elif isinstance(value, (int, float)):
                return datetime.fromtimestamp(value, tz=timezone.utc)
    
    return datetime.now(tz=timezone.utc)


def _parse_timestamp_string(timestamp_str: str) -> datetime:
    
    formats = [
        "%Y-%m-%d %H:%M:%S %Z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(timestamp_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    
    return datetime.now(tz=timezone.utc)


def _extract_media_type(item: dict[str, Any]) -> MediaType:
    
    type_keys = ["Media Type", "media_type", "type", "Type"]
    
    for key in type_keys:
        if key in item:
            value = str(item[key]).upper()
            
            if "IMAGE" in value or "PHOTO" in value or "JPG" in value or "PNG" in value:
                return MediaType.IMAGE
            elif "VIDEO" in value or "MP4" in value or "MOV" in value:
                return MediaType.VIDEO
    
    return MediaType.UNKNOWN


def _extract_download_url(item: dict[str, Any]) -> str | None:
    
    url_keys = ["Download Link", "download_link", "path", "file_path", "url"]
    
    for key in url_keys:
        if key in item and item[key]:
            return str(item[key])
    
    return None


def _extract_duration(item: dict[str, Any]) -> float | None:
    
    duration_keys = ["Duration", "duration", "length"]
    
    for key in duration_keys:
        if key in item:
            try:
                return float(item[key])
            except (ValueError, TypeError):
                pass
    
    return None


def _generate_filename(
    timestamp: datetime,
    media_type: MediaType,
    original_filename: str | None,
    memory_id: str
) -> str:
    
    date_str = timestamp.strftime("%Y%m%d_%H%M%S")
    
    if media_type == MediaType.IMAGE:
        extension = "jpg"
    elif media_type == MediaType.VIDEO:
        extension = "mp4"
    else:
        extension = "bin"
    
    if original_filename and isinstance(original_filename, str):
        parts = original_filename.rsplit(".", 1)
        if len(parts) == 2:
            extension = parts[1].lower()
    
    short_id = memory_id[:8]
    
    return f"{date_str}_{short_id}.{extension}"
