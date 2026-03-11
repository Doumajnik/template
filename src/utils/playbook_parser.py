"""Parse .playbook.md files with TOML frontmatter into structured chunk records."""

import os
import re
import hashlib
import tomllib

VALID_CATEGORIES = frozenset({
    "pattern", "anti-pattern", "rule", "convention", "decision", "strategy"
})

REQUIRED_FIELDS = ("id", "title", "agents", "technologies", "category", "tags", "version")

_FRONTMATTER_RE = re.compile(r"^\+\+\+\r?\n(.*?)\r?\n\+\+\+\r?\n(.*)", re.DOTALL)


def _extract_frontmatter(raw_text: str) -> tuple[dict, str]:
    """Split TOML frontmatter from markdown body using +++ delimiters."""
    match = _FRONTMATTER_RE.match(raw_text)
    if not match:
        raise ValueError("Missing +++ frontmatter delimiters")
    toml_text, body = match.group(1), match.group(2)
    try:
        metadata = tomllib.loads(toml_text)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Malformed TOML frontmatter: {exc}") from exc
    return metadata, body


def _validate_frontmatter(meta: dict, file_path: str) -> None:
    """Validate that all required frontmatter fields are present and well-typed."""
    for field in REQUIRED_FIELDS:
        if field not in meta:
            raise ValueError(f"Missing required field '{field}' in {file_path}")

    if not isinstance(meta["agents"], list):
        raise ValueError(f"'agents' must be a list in {file_path}")

    if not isinstance(meta["technologies"], list):
        raise ValueError(f"'technologies' must be a list in {file_path}")

    if not isinstance(meta["tags"], list):
        raise ValueError(f"'tags' must be a list in {file_path}")

    if not isinstance(meta["version"], int):
        raise ValueError(f"'version' must be an int in {file_path}")

    if meta["category"] not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category '{meta['category']}' in {file_path}. "
            f"Must be one of: {sorted(VALID_CATEGORIES)}"
        )


def _validate_content(body: str, file_path: str) -> None:
    """Validate that the markdown body is non-empty after stripping whitespace."""
    if not body.strip():
        raise ValueError(f"Empty playbook body in {file_path}")


def _compute_content_hash(content: str) -> str:
    """Compute a SHA-256 hex digest of the content with normalized newlines."""
    normalized = content.replace("\r\n", "\n").strip()
    hex_digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"sha256:{hex_digest}"


def _validate_unique_ids(chunks: list[dict]) -> None:
    """Check that all chunk id values are unique across parsed playbooks."""
    seen: dict[str, str] = {}
    for chunk in chunks:
        chunk_id = chunk["id"]
        if chunk_id in seen:
            raise ValueError(
                f"Duplicate id '{chunk_id}' found in "
                f"{seen[chunk_id]} and {chunk['source_file']}"
            )
        seen[chunk_id] = chunk["source_file"]


def parse_playbook_file(file_path: str) -> dict:
    """Parse a single .playbook.md file into a structured chunk record."""
    with open(file_path, encoding="utf-8") as f:
        raw_text = f.read()

    meta, body = _extract_frontmatter(raw_text)
    _validate_frontmatter(meta, file_path)
    _validate_content(body, file_path)
    content_hash = _compute_content_hash(body)

    return {
        "id": meta["id"],
        "title": meta["title"],
        "agents": meta["agents"],
        "technologies": meta["technologies"],
        "category": meta["category"],
        "tags": meta["tags"],
        "version": meta["version"],
        "content": body.strip(),
        "content_hash": content_hash,
        "source_file": file_path,
    }


def discover_playbook_files(base_dir: str) -> list[str]:
    """Recursively find all *.playbook.md files, skipping _ prefixed files."""
    results: list[str] = []
    for dirpath, _, filenames in os.walk(base_dir):
        for fname in filenames:
            if fname.endswith(".playbook.md") and not fname.startswith("_"):
                results.append(os.path.abspath(os.path.join(dirpath, fname)))
    return sorted(results)


def parse_all_playbooks(base_dir: str) -> list[dict]:
    """Discover and parse all playbook files, validating unique IDs."""
    paths = discover_playbook_files(base_dir)
    chunks = [parse_playbook_file(p) for p in paths]
    _validate_unique_ids(chunks)
    return chunks
