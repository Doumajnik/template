"""GitHub Models embedding API client with batching and retry logic.

Pure utility module — token is always passed explicitly, never read from env.
Uses only stdlib (urllib.request, json, time, sys).
"""

import json
import sys
import time
import urllib.error
import urllib.request

API_URL = "https://models.github.ai/inference/embeddings"
MODEL = "openai/text-embedding-3-small"
DIMENSIONS = 1536
MAX_BATCH_TOKENS = 54000  # Leave headroom below 64K limit
RATE_LIMIT_SLEEP = 4.0    # Seconds between batches (15 req/min limit)
MAX_RETRIES = 3
BASE_DELAY = 4.0          # Base delay for exponential backoff


def _estimate_tokens(text: str) -> int:
    """Rough token estimate based on character count. Minimum 1."""
    return max(1, len(text) // 4)


def _create_batches(
    texts: list[str],
    max_tokens: int = MAX_BATCH_TOKENS,
) -> list[list[tuple[int, str]]]:
    """Group texts into batches that fit under max_tokens.

    Each item is (original_index, text) to preserve ordering.
    A single text exceeding max_tokens gets its own batch.
    """
    batches: list[list[tuple[int, str]]] = []
    current_batch: list[tuple[int, str]] = []
    current_tokens = 0

    for idx, text in enumerate(texts):
        tokens = _estimate_tokens(text)
        if current_batch and current_tokens + tokens > max_tokens:
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append((idx, text))
        current_tokens += tokens

    if current_batch:
        batches.append(current_batch)
    return batches


def _call_embedding_api(
    batch_texts: list[str],
    token: str,
) -> list[list[float]]:
    """Single HTTP POST to the GitHub Models embedding API.

    Returns embeddings sorted by the response index field.
    Raises urllib.error.HTTPError on HTTP failures.
    """
    body = json.dumps({
        "input": batch_texts,
        "model": MODEL,
        "dimensions": DIMENSIONS,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    sorted_items = sorted(data["data"], key=lambda item: item["index"])
    return [item["embedding"] for item in sorted_items]


def _retry_with_backoff(
    func,
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
):
    """Call func() with exponential backoff on retryable errors.

    Retries on 429, 5xx, and network errors. Re-raises other 4xx immediately.
    """
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code == 429:
                retry_after = exc.headers.get("Retry-After")
                delay = (
                    float(retry_after)
                    if retry_after
                    else base_delay * (2 ** attempt)
                )
            elif 500 <= exc.code < 600:
                delay = base_delay * (2 ** attempt)
            else:
                raise
            if attempt >= max_retries:
                raise
            print(
                f"Retry {attempt + 1}/{max_retries} after {delay}s...",
                file=sys.stderr,
            )
            time.sleep(delay)
        except urllib.error.URLError as exc:
            last_exc = exc
            if attempt >= max_retries:
                raise
            delay = base_delay * (2 ** attempt)
            print(
                f"Retry {attempt + 1}/{max_retries} after {delay}s...",
                file=sys.stderr,
            )
            time.sleep(delay)

    raise last_exc  # pragma: no cover


def _rate_limit_sleep(batch_index: int) -> None:
    """Sleep between batches to respect rate limits. Batch 0 skips."""
    if batch_index > 0:
        time.sleep(RATE_LIMIT_SLEEP)


def embed_texts(texts: list[str], token: str) -> list[list[float]]:
    """Embed a list of texts, returning 1536-dim vectors in input order.

    Handles batching, rate limiting, and retry logic automatically.
    Token is passed explicitly — never read from environment.
    """
    if not texts:
        return []

    batches = _create_batches(texts)
    results: list[tuple[int, list[float]]] = []

    for batch_idx, batch in enumerate(batches):
        _rate_limit_sleep(batch_idx)
        batch_texts = [text for _, text in batch]
        embeddings = _retry_with_backoff(
            lambda bt=batch_texts: _call_embedding_api(bt, token),
        )
        for (orig_idx, _), embedding in zip(batch, embeddings):
            results.append((orig_idx, embedding))

    results.sort(key=lambda pair: pair[0])
    return [embedding for _, embedding in results]


def embed_single(text: str, token: str) -> list[float]:
    """Embed a single text string. Convenience wrapper around embed_texts."""
    return embed_texts([text], token)[0]
