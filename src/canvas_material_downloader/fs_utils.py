from __future__ import annotations

from pathlib import Path
import re
from typing import Any


INVALID_SEGMENT_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
MULTISPACE = re.compile(r"\s+")
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}
MAX_SEGMENT_LENGTH = 120


def sanitize_segment(value: str | None, fallback: str = "untitled") -> str:
    candidate = (value or "").strip()
    candidate = INVALID_SEGMENT_CHARS.sub("_", candidate)
    candidate = MULTISPACE.sub(" ", candidate)
    candidate = candidate.strip(" .")

    if not candidate:
        candidate = fallback

    stem, suffix = _split_suffix(candidate)
    if stem.upper() in WINDOWS_RESERVED_NAMES:
        stem = f"{stem}_"

    allowed_stem_length = max(1, MAX_SEGMENT_LENGTH - len(suffix))
    stem = stem[:allowed_stem_length].rstrip(" .") or fallback
    return f"{stem}{suffix}"


def course_directory_name(course: dict[str, Any]) -> str:
    parts = [
        str(course.get("id", "course")),
        course.get("course_code") or "",
        course.get("name") or "Untitled Course",
    ]
    cleaned = [sanitize_segment(part, fallback="course") for part in parts if str(part).strip()]
    return " - ".join(cleaned)


def file_destination_name(file_data: dict[str, Any]) -> str:
    file_id = str(file_data.get("id", "file"))
    display_name = file_data.get("display_name") or file_data.get("filename") or "download"
    return sanitize_segment(f"{file_id} - {display_name}", fallback=f"{file_id} - download")


def relative_display(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _split_suffix(filename: str) -> tuple[str, str]:
    if filename.startswith(".") or "." not in filename:
        return filename, ""

    stem, suffix = filename.rsplit(".", 1)
    if not stem or len(suffix) > 10:
        return filename, ""
    return stem, f".{suffix}"
