"""Knowledge index CRUD, incremental diffing, and similarity search."""

import datetime
import json
import os

INDEX_VERSION = 1
MODEL_NAME = "openai/text-embedding-3-small"
DIMENSIONS = 1536


def _empty_index() -> dict:
    """Return a valid empty index structure."""
    return {
        "version": INDEX_VERSION,
        "model": MODEL_NAME,
        "dimensions": DIMENSIONS,
        "built_at": "",
        "chunk_count": 0,
        "chunks": [],
    }


def _validate_index(index: dict) -> None:
    """Validate index structure and version. Raises ValueError if invalid."""
    required_keys = {"version", "model", "dimensions", "chunks"}
    missing = required_keys - set(index.keys())
    if missing:
        raise ValueError(f"Missing required keys: {missing}")
    if index["version"] != INDEX_VERSION:
        raise ValueError(
            f"Version mismatch: expected {INDEX_VERSION}, got {index['version']}"
        )


def filter_chunks(
    chunks: list[dict], agent: str | None, tech: str | None
) -> list[dict]:
    """Filter chunks by agent and/or technology (case-insensitive, AND logic)."""
    result = chunks
    if agent is not None:
        agent_lower = agent.lower()
        result = [
            c for c in result
            if agent_lower in [a.lower() for a in c.get("agents", [])]
            or "all" in [a.lower() for a in c.get("agents", [])]
        ]
    if tech is not None:
        tech_lower = tech.lower()
        result = [
            c for c in result
            if not c.get("technologies")
            or tech_lower in [t.lower() for t in c["technologies"]]
        ]
    return result


def _atomic_write(data: str, path: str) -> None:
    """Write data atomically via tmp-file + os.replace."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(tmp_path, path)


def _dot_product(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute dot product of two vectors (cosine sim for pre-normalized vecs)."""
    return sum(a * b for a, b in zip(vec_a, vec_b))


def _rank_by_similarity(
    query_vec: list[float], candidates: list[dict], top_k: int
) -> list[dict]:
    """Rank candidates by similarity to query_vec, return top_k results."""
    scored = [
        {**chunk, "score": _dot_product(query_vec, chunk["embedding"])}
        for chunk in candidates
    ]
    scored.sort(key=lambda c: c["score"], reverse=True)
    return scored[:top_k]


def load_index(index_path: str) -> dict:
    """Load and validate a knowledge index from disk. Returns empty index if missing."""
    if not os.path.exists(index_path):
        return _empty_index()
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Corrupted index: {index_path}") from exc
    _validate_index(index)
    return index


def save_index(index: dict, index_path: str) -> None:
    """Persist an index to disk atomically with updated timestamps."""
    index["built_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    index["chunk_count"] = len(index["chunks"])
    payload = json.dumps(index, separators=(",", ":"))
    _atomic_write(payload, index_path)


def diff_chunks(
    current_chunks: list[dict], existing_index: dict
) -> tuple[list[dict], list[str]]:
    """Compare current chunks against existing index. Returns (to_embed, to_remove)."""
    existing_map = {
        c["id"]: c.get("content_hash") for c in existing_index.get("chunks", [])
    }
    current_ids = set()
    chunks_to_embed: list[dict] = []

    for chunk in current_chunks:
        cid = chunk["id"]
        current_ids.add(cid)
        if cid not in existing_map or existing_map[cid] != chunk.get("content_hash"):
            chunks_to_embed.append(chunk)

    ids_to_remove = [eid for eid in existing_map if eid not in current_ids]
    return chunks_to_embed, ids_to_remove


def merge_embeddings(
    existing_index: dict,
    new_chunks: list[dict],
    embeddings: list[list[float]],
    removed_ids: list[str],
) -> dict:
    """Merge new embeddings into the index and remove stale chunks."""
    result = {**existing_index, "chunks": list(existing_index["chunks"])}
    result["chunks"] = [c for c in result["chunks"] if c["id"] not in set(removed_ids)]

    existing_ids = {c["id"]: i for i, c in enumerate(result["chunks"])}
    for chunk, embedding in zip(new_chunks, embeddings):
        entry = {**chunk, "embedding": embedding}
        if chunk["id"] in existing_ids:
            result["chunks"][existing_ids[chunk["id"]]] = entry
        else:
            result["chunks"].append(entry)
    return result


def search_chunks(
    index: dict,
    query_embedding: list[float],
    agent: str | None,
    tech: str | None,
    top_k: int,
) -> list[dict]:
    """Search index chunks by similarity, optionally filtered by agent/tech."""
    candidates = filter_chunks(index.get("chunks", []), agent, tech)
    return _rank_by_similarity(query_embedding, candidates, top_k)
