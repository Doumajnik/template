"""CI entry point: parse playbooks, compute incremental diff, embed, write index."""

import argparse
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"))

import embedding_client  # noqa: E402  # type: ignore[import-not-found]
import knowledge_index  # noqa: E402  # type: ignore[import-not-found]
import playbook_parser  # noqa: E402  # type: ignore[import-not-found]


def parse_args() -> argparse.Namespace:
    """Define and parse CLI arguments for the build pipeline."""
    parser = argparse.ArgumentParser(
        description="Build the RAG knowledge index from playbook files.",
    )
    parser.add_argument(
        "--playbooks-dir", default="docs/playbooks",
        help="Base directory for playbook files (default: docs/playbooks)",
    )
    parser.add_argument(
        "--index-path", default=".ai/knowledge-index.json",
        help="Output index file path (default: .ai/knowledge-index.json)",
    )
    parser.add_argument(
        "--full-rebuild", action="store_true",
        help="Force re-embedding all chunks (ignore content hashes)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Parse and diff only — don't call API or write index",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print detailed progress",
    )
    return parser.parse_args()


def validate_environment(args: argparse.Namespace) -> str | None:
    """Validate required env vars and paths. Returns the API token."""
    token = os.environ.get("GH_MODELS_TOKEN")
    if not token and not args.dry_run:
        print("Error: GH_MODELS_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.playbooks_dir):
        print(f"Error: Playbooks directory not found: {args.playbooks_dir}", file=sys.stderr)
        sys.exit(1)
    return token


def print_summary(total: int, embedded: int, removed: int, skipped: int) -> None:
    """Print a human-readable build summary to stdout."""
    print(f"Total chunks:   {total}")
    print(f"Embedded:       {embedded}")
    print(f"Removed:        {removed}")
    print(f"Skipped:        {skipped}")


def run_build(args: argparse.Namespace, token: str) -> None:
    """Core build pipeline: parse → diff → embed → merge → save."""
    if args.verbose:
        print("Parsing playbooks...", file=sys.stderr)
    chunks = playbook_parser.parse_all_playbooks(args.playbooks_dir)

    if args.verbose:
        print(f"Found {len(chunks)} chunks.", file=sys.stderr)

    existing = knowledge_index.load_index(args.index_path)

    if args.full_rebuild:
        to_embed = chunks
        to_remove = [
            c["id"] for c in existing.get("chunks", [])
            if c["id"] not in {ch["id"] for ch in chunks}
        ]
    else:
        to_embed, to_remove = knowledge_index.diff_chunks(chunks, existing)

    skipped = len(chunks) - len(to_embed)

    if args.verbose:
        print(f"To embed: {len(to_embed)}, to remove: {len(to_remove)}, skipped: {skipped}", file=sys.stderr)

    if args.dry_run:
        print("Dry run — no API calls or writes.", file=sys.stderr)
        print_summary(len(chunks), len(to_embed), len(to_remove), skipped)
        return

    if to_embed:
        if args.verbose:
            print("Calling embedding API...", file=sys.stderr)
        contents = [c["content"] for c in to_embed]
        embeddings = embedding_client.embed_texts(contents, token)
    else:
        embeddings = []

    merged = knowledge_index.merge_embeddings(existing, to_embed, embeddings, to_remove)

    if args.verbose:
        print(f"Saving index to {args.index_path}...", file=sys.stderr)
    knowledge_index.save_index(merged, args.index_path)

    print_summary(len(chunks), len(to_embed), len(to_remove), skipped)


def main() -> None:
    """Entry point: parse args, validate env, run build pipeline."""
    args = parse_args()
    token = validate_environment(args)
    try:
        run_build(args, token)
    except Exception as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
