"""CLI entry point for Librarian: load index, embed query, search, output results."""

import argparse
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"))

import embedding_client  # noqa: E402  # type: ignore[import-not-found]
import knowledge_index  # noqa: E402  # type: ignore[import-not-found]
from knowledge_index import filter_chunks  # noqa: E402  # type: ignore[import-not-found]
import playbook_parser  # noqa: E402  # type: ignore[import-not-found]


def parse_args() -> argparse.Namespace:
    """Define and parse CLI arguments for the query tool."""
    parser = argparse.ArgumentParser(
        description="Query the RAG knowledge index for relevant playbook chunks.",
    )
    parser.add_argument(
        "--query", required=True,
        help="The search query (required)",
    )
    parser.add_argument(
        "--agent", default=None,
        help="Filter to chunks relevant to this agent",
    )
    parser.add_argument(
        "--tech", default=None,
        help="Filter to chunks for this technology",
    )
    parser.add_argument(
        "--top-k", type=int, default=10,
        help="Number of results to return (default: 10)",
    )
    parser.add_argument(
        "--index-path", default=".ai/knowledge-index.json",
        help="Index file path (default: .ai/knowledge-index.json)",
    )
    parser.add_argument(
        "--playbooks-dir", default="docs/playbooks",
        help="Playbook files directory for fallback (default: docs/playbooks)",
    )
    parser.add_argument(
        "--format", default="markdown", choices=["markdown", "json"],
        help='Output format: "markdown" (default) or "json"',
    )
    return parser.parse_args()


def fallback_metadata_retrieval(
    playbooks_dir: str, agent: str | None, tech: str | None,
) -> list[dict]:
    """Return matching chunks using metadata-only filtering (no embeddings)."""
    print("\u26a0\ufe0f Using metadata-only fallback retrieval", file=sys.stderr)
    paths = playbook_parser.discover_playbook_files(playbooks_dir)
    chunks: list[dict] = []
    for path in paths:
        try:
            chunk = playbook_parser.parse_playbook_file(path)
        except ValueError:
            continue
        chunks.append(chunk)
    return filter_chunks(chunks, agent, tech)


def run_query(args: argparse.Namespace, token: str | None) -> list[dict]:
    """Run the query pipeline with graceful fallback on any failure."""
    if token is None:
        return fallback_metadata_retrieval(args.playbooks_dir, args.agent, args.tech)
    try:
        index = knowledge_index.load_index(args.index_path)
        query_embedding = embedding_client.embed_single(args.query, token)
        return knowledge_index.search_chunks(
            index, query_embedding, args.agent, args.tech, args.top_k,
        )
    except Exception as exc:
        print(f"Warning: {exc}", file=sys.stderr)
        return fallback_metadata_retrieval(args.playbooks_dir, args.agent, args.tech)


def format_results_markdown(results: list[dict]) -> str:
    """Format search results as readable Markdown."""
    if not results:
        return "No results found."
    lines: list[str] = []
    for r in results:
        score = r.get("score")
        title = r.get("title", "Untitled")
        chunk_id = r.get("id", "unknown")
        content = r.get("content", "")
        preview = content[:200] + "..." if len(content) > 200 else content
        source = r.get("source_file", "unknown")
        if score is not None:
            lines.append(f"**[Score: {score:.2f}]** {title} (`{chunk_id}`)")
        else:
            lines.append(f"**{title}** (`{chunk_id}`)")
        lines.append(f"> {preview}")
        lines.append("")
        lines.append(f"Source: {source}")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def format_results_json(results: list[dict]) -> str:
    """Format search results as JSON, stripping embedding vectors."""
    cleaned = []
    for r in results:
        entry = {k: v for k, v in r.items() if k != "embedding"}
        cleaned.append(entry)
    return json.dumps(cleaned, indent=2, default=str)


def main() -> None:
    """Entry point: parse args, run query, print formatted results."""
    args = parse_args()
    token = os.environ.get("GH_MODELS_TOKEN")
    results = run_query(args, token)
    if args.format == "json":
        print(format_results_json(results))
    else:
        print(format_results_markdown(results))


if __name__ == "__main__":
    main()
