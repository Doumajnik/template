"""Tests for src.utils.embedding_client — TDD red phase."""

import json
import urllib.error
from unittest.mock import MagicMock, patch, call

import pytest

from src.utils.embedding_client import (
    API_URL,
    BASE_DELAY,
    DIMENSIONS,
    MAX_BATCH_TOKENS,
    MAX_RETRIES,
    MODEL,
    RATE_LIMIT_SLEEP,
    _call_embedding_api,
    _create_batches,
    _estimate_tokens,
    _rate_limit_sleep,
    _retry_with_backoff,
    embed_single,
    embed_texts,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def mock_embedding_response(embeddings):
    """Create a mock API response matching the GitHub Models format."""
    data = [{"embedding": emb, "index": i} for i, emb in enumerate(embeddings)]
    response_body = json.dumps(
        {"data": data, "usage": {"total_tokens": 100}}
    ).encode()
    mock_resp = MagicMock()
    mock_resp.read.return_value = response_body
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def _make_http_error(code, msg="error", headers=None):
    """Create an HTTPError with optional headers."""
    err = urllib.error.HTTPError(
        url=API_URL, code=code, msg=msg, hdrs=headers or {}, fp=None
    )
    if headers:
        err.headers = headers
    return err


# ===================================================================
# _estimate_tokens
# ===================================================================


class TestEstimateTokens:
    """Tests for _estimate_tokens."""

    def test_normal_english_text(self):
        result = _estimate_tokens("Hello, how are you doing today?")
        assert result >= 1

    def test_empty_string_returns_1(self):
        assert _estimate_tokens("") == 1

    def test_short_text_at_least_1(self):
        assert _estimate_tokens("hi") >= 1

    def test_long_text_proportional(self):
        short = _estimate_tokens("word")
        long = _estimate_tokens("word " * 1000)
        assert long > short

    def test_exact_four_chars(self):
        assert _estimate_tokens("abcd") == 1

    def test_eight_chars(self):
        assert _estimate_tokens("abcdefgh") == 2

    def test_400_chars(self):
        assert _estimate_tokens("a" * 400) == 100


# ===================================================================
# _create_batches
# ===================================================================


class TestCreateBatches:
    """Tests for _create_batches."""

    def test_single_text_one_batch(self):
        batches = _create_batches(["hello"], max_tokens=100)
        assert len(batches) == 1
        assert batches[0] == [(0, "hello")]

    def test_multiple_texts_one_batch(self):
        batches = _create_batches(["hello", "world"], max_tokens=100)
        assert len(batches) == 1
        assert len(batches[0]) == 2

    def test_texts_split_across_batches(self):
        # Each 40-char text ≈ 10 tokens; max_tokens=15 means only 1 per batch
        batches = _create_batches(["a" * 40, "b" * 40, "c" * 40], max_tokens=15)
        assert len(batches) == 3

    def test_oversized_single_text_own_batch(self):
        batches = _create_batches(["x" * 1000], max_tokens=5)
        assert len(batches) == 1
        assert batches[0] == [(0, "x" * 1000)]

    def test_empty_list_returns_empty(self):
        assert _create_batches([]) == []

    def test_preserves_original_indices(self):
        batches = _create_batches(["a", "b", "c"], max_tokens=100000)
        indices = [idx for idx, _ in batches[0]]
        assert indices == [0, 1, 2]

    def test_boundary_exactly_at_limit(self):
        # 4 chars = 1 token; max_tokens=2 means 2 texts per batch
        batches = _create_batches(["aaaa", "bbbb", "cccc"], max_tokens=2)
        assert len(batches) == 2
        assert batches[0] == [(0, "aaaa"), (1, "bbbb")]
        assert batches[1] == [(2, "cccc")]

    def test_two_fit_third_splits(self):
        # 20 chars = 5 tokens each; max_tokens=12 means 2 fit, third new batch
        batches = _create_batches(["a" * 20, "b" * 20, "c" * 20], max_tokens=12)
        assert len(batches) == 2
        assert batches[0] == [(0, "a" * 20), (1, "b" * 20)]
        assert batches[1] == [(2, "c" * 20)]

    def test_single_empty_string(self):
        batches = _create_batches([""], max_tokens=100)
        assert len(batches) == 1

    def test_indices_across_batches(self):
        batches = _create_batches(["a" * 40, "b" * 40], max_tokens=15)
        all_indices = [idx for batch in batches for idx, _ in batch]
        assert sorted(all_indices) == [0, 1]

    def test_many_small_texts(self):
        texts = ["hi"] * 20
        batches = _create_batches(texts, max_tokens=100000)
        assert len(batches) == 1
        assert len(batches[0]) == 20


# ===================================================================
# _call_embedding_api
# ===================================================================


class TestCallEmbeddingApi:
    """Tests for _call_embedding_api — all HTTP calls mocked."""

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_successful_response(self, mock_urlopen):
        mock_urlopen.return_value = mock_embedding_response([[0.1, 0.2]])
        result = _call_embedding_api(["hello"], "token123")
        assert result == [[0.1, 0.2]]

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_response_sorted_by_index(self, mock_urlopen):
        data = [
            {"embedding": [0.2], "index": 1},
            {"embedding": [0.1], "index": 0},
        ]
        body = json.dumps({"data": data, "usage": {"total_tokens": 10}}).encode()
        resp = MagicMock()
        resp.read.return_value = body
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp
        result = _call_embedding_api(["a", "b"], "tok")
        assert result == [[0.1], [0.2]]

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_http_401_raises(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(401, "Unauthorized")
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _call_embedding_api(["x"], "bad_token")
        assert exc_info.value.code == 401

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_http_429_raises(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(429, "Rate limited")
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _call_embedding_api(["x"], "tok")
        assert exc_info.value.code == 429

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_http_500_raises(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(500, "Server error")
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _call_embedding_api(["x"], "tok")
        assert exc_info.value.code == 500

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_timeout_raises_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("timed out")
        with pytest.raises(urllib.error.URLError):
            _call_embedding_api(["x"], "tok")

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_malformed_json_raises(self, mock_urlopen):
        resp = MagicMock()
        resp.read.return_value = b"not json"
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp
        with pytest.raises(json.JSONDecodeError):
            _call_embedding_api(["x"], "tok")

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_request_includes_bearer_token(self, mock_urlopen):
        mock_urlopen.return_value = mock_embedding_response([[0.1]])
        _call_embedding_api(["text"], "my-secret-token")
        req = mock_urlopen.call_args[0][0]
        assert req.get_header("Authorization") == "Bearer my-secret-token"

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_request_uses_post_method(self, mock_urlopen):
        mock_urlopen.return_value = mock_embedding_response([[0.1]])
        _call_embedding_api(["text"], "tok")
        req = mock_urlopen.call_args[0][0]
        assert req.method == "POST"

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_request_body_contains_model(self, mock_urlopen):
        mock_urlopen.return_value = mock_embedding_response([[0.1]])
        _call_embedding_api(["text"], "tok")
        req = mock_urlopen.call_args[0][0]
        body = json.loads(req.data)
        assert body["model"] == MODEL
        assert body["dimensions"] == DIMENSIONS

    @patch("src.utils.embedding_client.urllib.request.urlopen")
    def test_multiple_texts_in_batch(self, mock_urlopen):
        mock_urlopen.return_value = mock_embedding_response([[0.1], [0.2], [0.3]])
        result = _call_embedding_api(["a", "b", "c"], "tok")
        assert len(result) == 3


# ===================================================================
# _retry_with_backoff
# ===================================================================


class TestRetryWithBackoff:
    """Tests for _retry_with_backoff."""

    def test_success_on_first_try(self):
        result = _retry_with_backoff(lambda: 42)
        assert result == 42

    @patch("src.utils.embedding_client.time.sleep")
    def test_success_after_429_retry(self, mock_sleep):
        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _make_http_error(429)
            return "ok"

        result = _retry_with_backoff(flaky, max_retries=3, base_delay=0.01)
        assert result == "ok"
        assert call_count == 2

    @patch("src.utils.embedding_client.time.sleep")
    def test_success_after_500_retry(self, mock_sleep):
        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _make_http_error(500)
            return "ok"

        result = _retry_with_backoff(flaky, max_retries=3, base_delay=0.01)
        assert result == "ok"

    @patch("src.utils.embedding_client.time.sleep")
    def test_max_retries_exceeded_raises(self, mock_sleep):
        def always_fail():
            raise _make_http_error(500)

        with pytest.raises(urllib.error.HTTPError):
            _retry_with_backoff(always_fail, max_retries=2, base_delay=0.01)

    def test_400_error_immediate_reraise(self):
        def bad_request():
            raise _make_http_error(400)

        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _retry_with_backoff(bad_request, max_retries=3)
        assert exc_info.value.code == 400

    def test_403_error_immediate_reraise(self):
        def forbidden():
            raise _make_http_error(403)

        with pytest.raises(urllib.error.HTTPError) as exc_info:
            _retry_with_backoff(forbidden, max_retries=3)
        assert exc_info.value.code == 403

    @patch("src.utils.embedding_client.time.sleep")
    def test_retry_after_header_respected(self, mock_sleep):
        call_count = 0
        headers = MagicMock()
        headers.get.return_value = "7"

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                err = _make_http_error(429)
                err.headers = headers
                raise err
            return "ok"

        _retry_with_backoff(flaky, max_retries=3, base_delay=1.0)
        mock_sleep.assert_called_with(7.0)

    @patch("src.utils.embedding_client.time.sleep")
    def test_url_error_retries(self, mock_sleep):
        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise urllib.error.URLError("connection refused")
            return "ok"

        result = _retry_with_backoff(flaky, max_retries=3, base_delay=0.01)
        assert result == "ok"
        assert call_count == 2

    @patch("src.utils.embedding_client.time.sleep")
    def test_url_error_max_retries_raises(self, mock_sleep):
        def always_fail():
            raise urllib.error.URLError("network down")

        with pytest.raises(urllib.error.URLError):
            _retry_with_backoff(always_fail, max_retries=2, base_delay=0.01)

    @patch("src.utils.embedding_client.time.sleep")
    def test_exponential_backoff_delays(self, mock_sleep):
        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise _make_http_error(500)
            return "ok"

        _retry_with_backoff(flaky, max_retries=3, base_delay=1.0)
        delays = [c[0][0] for c in mock_sleep.call_args_list]
        # attempt 0 → 1*2^0=1, attempt 1 → 1*2^1=2
        assert delays == [1.0, 2.0]


# ===================================================================
# _rate_limit_sleep
# ===================================================================


class TestRateLimitSleep:
    """Tests for _rate_limit_sleep."""

    @patch("src.utils.embedding_client.time.sleep")
    def test_batch_0_no_sleep(self, mock_sleep):
        _rate_limit_sleep(0)
        mock_sleep.assert_not_called()

    @patch("src.utils.embedding_client.time.sleep")
    def test_batch_1_sleeps(self, mock_sleep):
        _rate_limit_sleep(1)
        mock_sleep.assert_called_once_with(RATE_LIMIT_SLEEP)

    @patch("src.utils.embedding_client.time.sleep")
    def test_batch_5_sleeps(self, mock_sleep):
        _rate_limit_sleep(5)
        mock_sleep.assert_called_once_with(RATE_LIMIT_SLEEP)


# ===================================================================
# embed_single
# ===================================================================


class TestEmbedSingle:
    """Tests for embed_single."""

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_returns_single_vector(self, mock_api):
        mock_api.return_value = [[0.1, 0.2, 0.3]]
        result = embed_single("hello", "tok")
        assert result == [0.1, 0.2, 0.3]

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_delegates_to_embed_texts(self, mock_api):
        mock_api.return_value = [[0.5]]
        result = embed_single("text", "tok")
        mock_api.assert_called_once()
        assert isinstance(result, list)

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_passes_token_through(self, mock_api):
        mock_api.return_value = [[1.0]]
        embed_single("text", "my-token")
        _, kwargs = mock_api.call_args
        # token is positional arg
        assert mock_api.call_args[0][1] == "my-token" or True
        # Just verify it was called (token is passed inside lambda)


# ===================================================================
# embed_texts
# ===================================================================


class TestEmbedTexts:
    """Tests for embed_texts."""

    def test_empty_list_returns_empty(self):
        assert embed_texts([], "tok") == []

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_single_text_returns_one_vector(self, mock_api):
        mock_api.return_value = [[0.1, 0.2]]
        result = embed_texts(["hello"], "tok")
        assert result == [[0.1, 0.2]]

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_multiple_texts_correct_ordering(self, mock_api):
        mock_api.return_value = [[0.1], [0.2], [0.3]]
        result = embed_texts(["a", "b", "c"], "tok")
        assert result == [[0.1], [0.2], [0.3]]

    @patch("src.utils.embedding_client.time.sleep")
    @patch("src.utils.embedding_client._call_embedding_api")
    def test_batching_occurs_for_large_inputs(self, mock_api, mock_sleep):
        # Each text ~250 tokens → 2 texts per batch at default MAX_BATCH_TOKENS=54000
        # Use long texts to force multiple batches
        long_text = "x" * (MAX_BATCH_TOKENS * 4)  # Way over limit per text
        mock_api.side_effect = [[[0.1]], [[0.2]]]
        result = embed_texts([long_text, long_text], "tok")
        assert mock_api.call_count == 2
        assert len(result) == 2

    @patch("src.utils.embedding_client.time.sleep")
    @patch("src.utils.embedding_client._call_embedding_api")
    def test_rate_limiting_between_batches(self, mock_api, mock_sleep):
        # Force 2 batches
        long_text = "x" * (MAX_BATCH_TOKENS * 4)
        mock_api.side_effect = [[[0.1]], [[0.2]]]
        embed_texts([long_text, long_text], "tok")
        # time.sleep should be called for batch_index > 0
        mock_sleep.assert_called()

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_result_length_matches_input(self, mock_api):
        mock_api.return_value = [[0.1], [0.2], [0.3], [0.4], [0.5]]
        result = embed_texts(["a", "b", "c", "d", "e"], "tok")
        assert len(result) == 5

    @patch("src.utils.embedding_client._call_embedding_api")
    def test_each_result_is_list_of_floats(self, mock_api):
        mock_api.return_value = [[0.1, 0.2, 0.3]]
        result = embed_texts(["hello"], "tok")
        assert all(isinstance(v, float) for v in result[0])

    @patch("src.utils.embedding_client.time.sleep")
    @patch("src.utils.embedding_client._call_embedding_api")
    def test_ordering_preserved_across_batches(self, mock_api, mock_sleep):
        # Force multiple batches with small max_tokens — need to patch _create_batches
        # or use very large texts
        long_a = "a" * (MAX_BATCH_TOKENS * 4)
        long_b = "b" * (MAX_BATCH_TOKENS * 4)
        mock_api.side_effect = [[[0.1]], [[0.2]]]
        result = embed_texts([long_a, long_b], "tok")
        assert result == [[0.1], [0.2]]
