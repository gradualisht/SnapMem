from core.models import ExportSummary, ErrorRecord, WarningRecord, SkippedItem


def merge_summaries(*summaries: ExportSummary) -> ExportSummary:
    
    merged = ExportSummary()
    
    for summary in summaries:
        merged.total_memories_found += summary.total_memories_found
        merged.successful_exports += summary.successful_exports
        merged.failed_exports += summary.failed_exports
        merged.warnings_count += summary.warnings_count
        merged.skipped_count += summary.skipped_count
        
        merged.errors.extend(summary.errors)
        merged.warnings.extend(summary.warnings)
        merged.skipped.extend(summary.skipped)
        merged.successes.extend(summary.successes)
    
    return merged


def create_summary_from_parts(
    memories_found: int = 0,
    warnings: list[WarningRecord] | None = None,
    skipped: list[SkippedItem] | None = None,
    errors: list[ErrorRecord] | None = None
) -> ExportSummary:
    
    summary = ExportSummary()
    summary.total_memories_found = memories_found
    
    if warnings:
        summary.warnings = list(warnings)
        summary.warnings_count = len(warnings)
    
    if skipped:
        summary.skipped = list(skipped)
        summary.skipped_count = len(skipped)
    
    if errors:
        summary.errors = list(errors)
        summary.failed_exports = len(errors)
    
    return summary


def format_summary(summary: ExportSummary) -> str:
    
    lines = []
    
    lines.append("=" * 60)
    lines.append("SnapMem Export Summary")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append(f"Total memories found:    {summary.total_memories_found}")
    lines.append(f"Successfully exported:   {summary.successful_exports}")
    lines.append(f"Failed exports:          {summary.failed_exports}")
    lines.append(f"Warnings:                {summary.warnings_count}")
    lines.append(f"Skipped items:           {summary.skipped_count}")
    lines.append("")
    
    if summary.errors:
        lines.append("-" * 60)
        lines.append("ERRORS:")
        lines.append("-" * 60)
        for error in summary.errors:
            lines.append(f"  [{error.error_type}] {error.item_id}")
            lines.append(f"    {error.message}")
            if error.context:
                lines.append(f"    Context: {error.context}")
        lines.append("")
    
    if summary.warnings:
        lines.append("-" * 60)
        lines.append("WARNINGS:")
        lines.append("-" * 60)
        for warning in summary.warnings:
            lines.append(f"  [{warning.warning_type}] {warning.item_id}")
            lines.append(f"    {warning.message}")
        lines.append("")
    
    if summary.skipped:
        lines.append("-" * 60)
        lines.append("SKIPPED:")
        lines.append("-" * 60)
        for skipped in summary.skipped:
            lines.append(f"  [{skipped.reason}] {skipped.item_id}")
            if skipped.details:
                lines.append(f"    {skipped.details}")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def format_summary_brief(summary: ExportSummary) -> str:
    
    status = "SUCCESS" if summary.failed_exports == 0 else "COMPLETED WITH ERRORS"
    
    lines = [
        f"Export {status}",
        f"  {summary.successful_exports}/{summary.total_memories_found} exported",
    ]
    
    if summary.failed_exports > 0:
        lines.append(f"  {summary.failed_exports} failed")
    if summary.warnings_count > 0:
        lines.append(f"  {summary.warnings_count} warnings")
    if summary.skipped_count > 0:
        lines.append(f"  {summary.skipped_count} skipped")
    
    return "\n".join(lines)
