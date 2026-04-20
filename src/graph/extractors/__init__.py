"""Extractor registry. Dispatches by file extension to the correct parser."""

from collections.abc import Callable
from pathlib import Path

from src.graph.extractors.js_ts import extract_js_ts
from src.graph.extractors.python_ast import extract_python
from src.graph.models import Edge, Node

# Map of file suffix -> extractor callable.
# An extractor takes (file_path: str, source_text: str) and returns (nodes, edges).
ExtractorFn = Callable[[str, str], tuple[list[Node], list[Edge]]]

EXTRACTORS: dict[str, ExtractorFn] = {
    ".py": extract_python,
    ".js": lambda p, s: extract_js_ts(p, s, "javascript"),
    ".jsx": lambda p, s: extract_js_ts(p, s, "javascript"),
    ".mjs": lambda p, s: extract_js_ts(p, s, "javascript"),
    ".cjs": lambda p, s: extract_js_ts(p, s, "javascript"),
    ".ts": lambda p, s: extract_js_ts(p, s, "typescript"),
    ".tsx": lambda p, s: extract_js_ts(p, s, "tsx"),
}


def get_extractor(file_path: str) -> ExtractorFn | None:
    """Return the extractor for ``file_path`` or None if unsupported."""
    return EXTRACTORS.get(Path(file_path).suffix.lower())


def supported_suffixes() -> list[str]:
    """Return all file suffixes a registered extractor can handle."""
    return sorted(EXTRACTORS.keys())
