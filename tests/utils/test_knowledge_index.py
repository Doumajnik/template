"""Comprehensive tests for src/utils/knowledge_index.py."""

import json
import os

import pytest

from src.utils.knowledge_index import (
    DIMENSIONS,
    INDEX_VERSION,
    MODEL_NAME,
    _atomic_write,
    _dot_product,
    _empty_index,
    filter_chunks,
    _rank_by_similarity,
    _validate_index,
    diff_chunks,
    load_index,
    merge_embeddings,
    save_index,
    search_chunks,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

_UNSET = object()


def make_chunk(
    id,
    agents=_UNSET,
    technologies=_UNSET,
    content_hash="sha256:abc",
    embedding=None,
    content="Test content",
):
    return {
        "id": id,
        "title": f"Test {id}",
        "agents": ["all"] if agents is _UNSET else agents,
        "technologies": ["all"] if technologies is _UNSET else technologies,
        "category": "rule",
        "tags": ["test"],
        "content": content,
        "content_hash": content_hash,
        "source_file": f"test/{id}.playbook.md",
        "embedding": embedding or [0.0] * DIMENSIONS,
    }


def make_index(chunks=None):
    return {
        "version": INDEX_VERSION,
        "model": MODEL_NAME,
        "dimensions": DIMENSIONS,
        "built_at": "2026-01-01T00:00:00+00:00",
        "chunk_count": len(chunks or []),
        "chunks": chunks or [],
    }


# ===================================================================
# TestEmptyIndex
# ===================================================================

class TestEmptyIndex:
    def test_returns_dict_with_all_required_keys(self):
        idx = _empty_index()
        for key in ("version", "model", "dimensions", "built_at", "chunk_count", "chunks"):
            assert key in idx, f"Missing key: {key}"

    def test_has_correct_version_model_dimensions(self):
        idx = _empty_index()
        assert idx["version"] == INDEX_VERSION
        assert idx["model"] == MODEL_NAME
        assert idx["dimensions"] == DIMENSIONS

    def test_has_empty_chunks_list(self):
        idx = _empty_index()
        assert idx["chunks"] == []
        assert idx["chunk_count"] == 0

    def test_built_at_is_empty_string(self):
        idx = _empty_index()
        assert idx["built_at"] == ""

    def test_returns_new_dict_each_call(self):
        a = _empty_index()
        b = _empty_index()
        assert a is not b
        a["chunks"].append("x")
        assert b["chunks"] == []


# ===================================================================
# TestValidateIndex
# ===================================================================

class TestValidateIndex:
    def test_valid_index_passes(self):
        _validate_index(make_index())  # should not raise

    def test_missing_version_raises(self):
        idx = make_index()
        del idx["version"]
        with pytest.raises(ValueError, match="Missing required keys"):
            _validate_index(idx)

    def test_wrong_version_raises(self):
        idx = make_index()
        idx["version"] = 999
        with pytest.raises(ValueError, match="Version mismatch"):
            _validate_index(idx)

    def test_missing_chunks_raises(self):
        idx = make_index()
        del idx["chunks"]
        with pytest.raises(ValueError, match="Missing required keys"):
            _validate_index(idx)

    def test_missing_model_raises(self):
        idx = make_index()
        del idx["model"]
        with pytest.raises(ValueError, match="Missing required keys"):
            _validate_index(idx)

    def test_missing_dimensions_raises(self):
        idx = make_index()
        del idx["dimensions"]
        with pytest.raises(ValueError, match="Missing required keys"):
            _validate_index(idx)

    def test_valid_index_with_chunks_passes(self):
        idx = make_index(chunks=[make_chunk("c1")])
        _validate_index(idx)  # should not raise

    def test_missing_multiple_keys_raises(self):
        idx = {"built_at": "", "chunk_count": 0}
        with pytest.raises(ValueError, match="Missing required keys"):
            _validate_index(idx)


# ===================================================================
# TestFilterChunks
# ===================================================================

class TestFilterChunks:
    def setup_method(self):
        self.chunks = [
            make_chunk("c1", agents=["Worker"], technologies=["python"]),
            make_chunk("c2", agents=["Reviewer"], technologies=["typescript"]),
            make_chunk("c3", agents=["all"], technologies=["python", "go"]),
            make_chunk("c4", agents=["Worker", "Debug"], technologies=[]),
        ]

    def test_no_filters_returns_all(self):
        assert filter_chunks(self.chunks, None, None) == self.chunks

    def test_filter_by_agent_only_matching(self):
        result = filter_chunks(self.chunks, "Worker", None)
        ids = [c["id"] for c in result]
        assert "c1" in ids
        assert "c4" in ids
        # c3 has agent "all" so it should also match
        assert "c3" in ids
        assert "c2" not in ids

    def test_agent_filter_case_insensitive(self):
        result = filter_chunks(self.chunks, "worker", None)
        ids = [c["id"] for c in result]
        assert "c1" in ids

    def test_agent_all_matches_any_filter(self):
        result = filter_chunks(self.chunks, "SomeRandomAgent", None)
        ids = [c["id"] for c in result]
        assert "c3" in ids  # has agents=["all"]

    def test_filter_by_tech_only_matching(self):
        result = filter_chunks(self.chunks, None, "python")
        ids = [c["id"] for c in result]
        assert "c1" in ids
        assert "c3" in ids
        assert "c2" not in ids

    def test_tech_filter_case_insensitive(self):
        result = filter_chunks(self.chunks, None, "Python")
        ids = [c["id"] for c in result]
        assert "c1" in ids

    def test_empty_technologies_matches_any_tech_filter(self):
        result = filter_chunks(self.chunks, None, "java")
        ids = [c["id"] for c in result]
        # c4 has technologies=[] so it matches any tech filter
        assert "c4" in ids

    def test_combined_agent_and_tech_filter(self):
        result = filter_chunks(self.chunks, "Worker", "python")
        ids = [c["id"] for c in result]
        # c1: agent=Worker, tech=python → match
        assert "c1" in ids
        # c3: agent=all, tech=python → match
        assert "c3" in ids
        # c4: agent=Worker, tech=[] → match (empty tech matches any)
        assert "c4" in ids
        # c2: agent=Reviewer → no
        assert "c2" not in ids

    def test_no_matches_returns_empty(self):
        chunks = [
            make_chunk("x", agents=["Reviewer"], technologies=["typescript"]),
        ]
        result = filter_chunks(chunks, "Reviewer", "python")
        assert result == []

    def test_empty_input_returns_empty(self):
        assert filter_chunks([], "Worker", "python") == []

    def test_filter_by_agent_not_present(self):
        result = filter_chunks(
            [make_chunk("x", agents=["Debug"], technologies=["go"])],
            "Architect",
            None,
        )
        assert result == []


# ===================================================================
# TestAtomicWrite
# ===================================================================

class TestAtomicWrite:
    def test_writes_content_to_file(self, tmp_path):
        p = str(tmp_path / "out.txt")
        _atomic_write("hello world", p)
        assert os.path.exists(p)

    def test_file_content_matches_input(self, tmp_path):
        p = str(tmp_path / "out.txt")
        _atomic_write("hello world", p)
        assert open(p, encoding="utf-8").read() == "hello world"

    def test_creates_parent_directories(self, tmp_path):
        p = str(tmp_path / "sub" / "dir" / "out.txt")
        _atomic_write("nested", p)
        assert open(p, encoding="utf-8").read() == "nested"

    def test_overwrites_existing_file(self, tmp_path):
        p = str(tmp_path / "out.txt")
        _atomic_write("first", p)
        _atomic_write("second", p)
        assert open(p, encoding="utf-8").read() == "second"

    def test_no_tmp_file_left_after_success(self, tmp_path):
        p = str(tmp_path / "out.txt")
        _atomic_write("data", p)
        assert not os.path.exists(f"{p}.tmp")

    def test_writes_unicode_content(self, tmp_path):
        p = str(tmp_path / "unicode.txt")
        _atomic_write("café ☕ 日本語", p)
        assert open(p, encoding="utf-8").read() == "café ☕ 日本語"


# ===================================================================
# TestDotProduct
# ===================================================================

class TestDotProduct:
    def test_identical_unit_vectors(self):
        v = [1.0, 0.0, 0.0]
        assert _dot_product(v, v) == pytest.approx(1.0)

    def test_orthogonal_vectors(self):
        assert _dot_product([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)

    def test_known_values(self):
        assert _dot_product([1, 2, 3], [4, 5, 6]) == pytest.approx(32.0)

    def test_zero_vector(self):
        assert _dot_product([0, 0, 0], [1, 2, 3]) == pytest.approx(0.0)

    def test_negative_values(self):
        assert _dot_product([-1, -2], [3, 4]) == pytest.approx(-11.0)

    def test_single_element(self):
        assert _dot_product([5.0], [3.0]) == pytest.approx(15.0)

    def test_symmetric(self):
        a, b = [1, 2, 3], [4, 5, 6]
        assert _dot_product(a, b) == pytest.approx(_dot_product(b, a))


# ===================================================================
# TestRankBySimilarity
# ===================================================================

class TestRankBySimilarity:
    def _make_candidate(self, id, embedding):
        return make_chunk(id, embedding=embedding)

    def test_correct_ordering_highest_first(self):
        q = [1.0, 0.0, 0.0]
        candidates = [
            self._make_candidate("low", [0.1, 0.0, 0.0]),
            self._make_candidate("high", [0.9, 0.0, 0.0]),
            self._make_candidate("mid", [0.5, 0.0, 0.0]),
        ]
        result = _rank_by_similarity(q, candidates, 3)
        assert result[0]["id"] == "high"
        assert result[1]["id"] == "mid"
        assert result[2]["id"] == "low"

    def test_top_k_limits_results(self):
        q = [1.0, 0.0]
        candidates = [
            self._make_candidate("a", [0.1, 0.0]),
            self._make_candidate("b", [0.5, 0.0]),
            self._make_candidate("c", [0.9, 0.0]),
        ]
        result = _rank_by_similarity(q, candidates, 2)
        assert len(result) == 2

    def test_score_key_added(self):
        q = [1.0, 0.0]
        candidates = [self._make_candidate("a", [0.5, 0.0])]
        result = _rank_by_similarity(q, candidates, 1)
        assert "score" in result[0]

    def test_does_not_mutate_original_dicts(self):
        q = [1.0, 0.0]
        original = self._make_candidate("a", [0.5, 0.0])
        _ = _rank_by_similarity(q, [original], 1)
        assert "score" not in original

    def test_empty_candidates_returns_empty(self):
        assert _rank_by_similarity([1.0], [], 5) == []

    def test_single_candidate(self):
        q = [1.0]
        candidates = [self._make_candidate("only", [0.7])]
        result = _rank_by_similarity(q, candidates, 5)
        assert len(result) == 1
        assert result[0]["id"] == "only"

    def test_top_k_larger_than_candidates(self):
        q = [1.0]
        candidates = [
            self._make_candidate("a", [0.1]),
            self._make_candidate("b", [0.9]),
        ]
        result = _rank_by_similarity(q, candidates, 100)
        assert len(result) == 2

    def test_correct_scores_assigned(self):
        q = [1.0, 0.0]
        candidates = [self._make_candidate("a", [0.3, 0.4])]
        result = _rank_by_similarity(q, candidates, 1)
        assert result[0]["score"] == pytest.approx(0.3)

    def test_zero_top_k_returns_empty(self):
        q = [1.0]
        candidates = [self._make_candidate("a", [0.5])]
        assert _rank_by_similarity(q, candidates, 0) == []


# ===================================================================
# TestLoadIndex
# ===================================================================

class TestLoadIndex:
    def test_missing_file_returns_empty_index(self, tmp_path):
        idx = load_index(str(tmp_path / "nope.json"))
        assert idx["version"] == INDEX_VERSION
        assert idx["chunks"] == []

    def test_valid_json_file_returns_parsed(self, tmp_path):
        p = tmp_path / "idx.json"
        data = make_index(chunks=[make_chunk("c1")])
        p.write_text(json.dumps(data), encoding="utf-8")
        idx = load_index(str(p))
        assert idx["version"] == INDEX_VERSION
        assert len(idx["chunks"]) == 1

    def test_corrupted_json_raises_valueerror(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{not valid json", encoding="utf-8")
        with pytest.raises(ValueError, match="Corrupted index"):
            load_index(str(p))

    def test_invalid_schema_version_raises(self, tmp_path):
        p = tmp_path / "v2.json"
        data = make_index()
        data["version"] = 99
        p.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ValueError, match="Version mismatch"):
            load_index(str(p))

    def test_valid_file_preserves_built_at(self, tmp_path):
        p = tmp_path / "idx.json"
        data = make_index()
        data["built_at"] = "2026-06-15T12:00:00+00:00"
        p.write_text(json.dumps(data), encoding="utf-8")
        idx = load_index(str(p))
        assert idx["built_at"] == "2026-06-15T12:00:00+00:00"


# ===================================================================
# TestSaveIndex
# ===================================================================

class TestSaveIndex:
    def test_writes_valid_json(self, tmp_path):
        p = str(tmp_path / "out.json")
        idx = make_index()
        save_index(idx, p)
        loaded = json.loads(open(p, encoding="utf-8").read())
        assert loaded["version"] == INDEX_VERSION

    def test_updates_built_at_timestamp(self, tmp_path):
        p = str(tmp_path / "out.json")
        idx = make_index()
        save_index(idx, p)
        assert idx["built_at"] != ""
        assert "T" in idx["built_at"]  # ISO format

    def test_updates_chunk_count(self, tmp_path):
        p = str(tmp_path / "out.json")
        idx = make_index(chunks=[make_chunk("c1"), make_chunk("c2")])
        save_index(idx, p)
        loaded = json.loads(open(p, encoding="utf-8").read())
        assert loaded["chunk_count"] == 2

    def test_atomic_write_file_exists(self, tmp_path):
        p = str(tmp_path / "out.json")
        save_index(make_index(), p)
        assert os.path.exists(p)
        assert not os.path.exists(f"{p}.tmp")

    def test_creates_parent_dirs(self, tmp_path):
        p = str(tmp_path / "nested" / "dir" / "out.json")
        save_index(make_index(), p)
        assert os.path.exists(p)

    def test_roundtrip_load_save(self, tmp_path):
        p = str(tmp_path / "rt.json")
        original = make_index(chunks=[make_chunk("c1")])
        save_index(original, p)
        loaded = load_index(p)
        assert loaded["version"] == INDEX_VERSION
        assert len(loaded["chunks"]) == 1


# ===================================================================
# TestDiffChunks
# ===================================================================

class TestDiffChunks:
    def test_new_chunk_in_to_embed(self):
        current = [make_chunk("new1")]
        existing = make_index()
        to_embed, to_remove = diff_chunks(current, existing)
        assert len(to_embed) == 1
        assert to_embed[0]["id"] == "new1"
        assert to_remove == []

    def test_changed_chunk_in_to_embed(self):
        current = [make_chunk("c1", content_hash="sha256:changed")]
        existing = make_index(chunks=[make_chunk("c1", content_hash="sha256:original")])
        to_embed, to_remove = diff_chunks(current, existing)
        assert len(to_embed) == 1
        assert to_embed[0]["id"] == "c1"

    def test_unchanged_chunk_skipped(self):
        chunk = make_chunk("c1", content_hash="sha256:same")
        current = [chunk]
        existing = make_index(chunks=[make_chunk("c1", content_hash="sha256:same")])
        to_embed, to_remove = diff_chunks(current, existing)
        assert to_embed == []
        assert to_remove == []

    def test_removed_chunk_in_to_remove(self):
        current = []
        existing = make_index(chunks=[make_chunk("old1")])
        to_embed, to_remove = diff_chunks(current, existing)
        assert to_embed == []
        assert "old1" in to_remove

    def test_empty_existing_all_new(self):
        current = [make_chunk("a"), make_chunk("b")]
        existing = make_index()
        to_embed, to_remove = diff_chunks(current, existing)
        assert len(to_embed) == 2
        assert to_remove == []

    def test_empty_current_all_removed(self):
        existing = make_index(chunks=[make_chunk("x"), make_chunk("y")])
        to_embed, to_remove = diff_chunks([], existing)
        assert to_embed == []
        assert set(to_remove) == {"x", "y"}

    def test_mixed_scenario(self):
        current = [
            make_chunk("unchanged", content_hash="sha256:same"),
            make_chunk("changed", content_hash="sha256:new_hash"),
            make_chunk("brand_new", content_hash="sha256:nn"),
        ]
        existing = make_index(chunks=[
            make_chunk("unchanged", content_hash="sha256:same"),
            make_chunk("changed", content_hash="sha256:old_hash"),
            make_chunk("stale", content_hash="sha256:gone"),
        ])
        to_embed, to_remove = diff_chunks(current, existing)
        embed_ids = {c["id"] for c in to_embed}
        assert embed_ids == {"changed", "brand_new"}
        assert to_remove == ["stale"]

    def test_returns_tuple(self):
        result = diff_chunks([], make_index())
        assert isinstance(result, tuple)
        assert len(result) == 2


# ===================================================================
# TestMergeEmbeddings
# ===================================================================

class TestMergeEmbeddings:
    def test_adds_new_chunk_with_embedding(self):
        existing = make_index()
        new_chunks = [make_chunk("c1")]
        embeddings = [[1.0] * DIMENSIONS]
        result = merge_embeddings(existing, new_chunks, embeddings, [])
        assert len(result["chunks"]) == 1
        assert result["chunks"][0]["id"] == "c1"
        assert result["chunks"][0]["embedding"] == [1.0] * DIMENSIONS

    def test_removes_stale_id(self):
        existing = make_index(chunks=[make_chunk("old")])
        result = merge_embeddings(existing, [], [], ["old"])
        assert len(result["chunks"]) == 0

    def test_preserves_unchanged_chunks(self):
        existing = make_index(chunks=[make_chunk("keep", embedding=[0.5] * DIMENSIONS)])
        result = merge_embeddings(existing, [], [], [])
        assert len(result["chunks"]) == 1
        assert result["chunks"][0]["id"] == "keep"

    def test_updates_existing_chunk_with_new_embedding(self):
        existing = make_index(chunks=[make_chunk("c1", embedding=[0.0] * DIMENSIONS)])
        new_chunks = [make_chunk("c1")]
        embeddings = [[1.0] * DIMENSIONS]
        result = merge_embeddings(existing, new_chunks, embeddings, [])
        assert len(result["chunks"]) == 1
        assert result["chunks"][0]["embedding"] == [1.0] * DIMENSIONS

    def test_empty_new_and_empty_removed_unchanged(self):
        existing = make_index(chunks=[make_chunk("c1")])
        result = merge_embeddings(existing, [], [], [])
        assert len(result["chunks"]) == 1
        assert result["chunks"][0]["id"] == "c1"

    def test_multiple_operations_in_one_merge(self):
        existing = make_index(chunks=[
            make_chunk("keep", embedding=[0.1] * DIMENSIONS),
            make_chunk("remove_me", embedding=[0.2] * DIMENSIONS),
            make_chunk("update_me", embedding=[0.3] * DIMENSIONS),
        ])
        new_chunks = [
            make_chunk("update_me"),
            make_chunk("brand_new"),
        ]
        embeddings = [
            [0.9] * DIMENSIONS,
            [0.8] * DIMENSIONS,
        ]
        result = merge_embeddings(existing, new_chunks, embeddings, ["remove_me"])
        ids = [c["id"] for c in result["chunks"]]
        assert "keep" in ids
        assert "remove_me" not in ids
        assert "update_me" in ids
        assert "brand_new" in ids
        updated = next(c for c in result["chunks"] if c["id"] == "update_me")
        assert updated["embedding"] == [0.9] * DIMENSIONS

    def test_embedding_vector_stored_correctly(self):
        emb = [float(i) for i in range(DIMENSIONS)]
        result = merge_embeddings(make_index(), [make_chunk("c1")], [emb], [])
        assert result["chunks"][0]["embedding"] == emb

    def test_does_not_mutate_existing_index(self):
        existing = make_index(chunks=[make_chunk("c1")])
        original_len = len(existing["chunks"])
        merge_embeddings(existing, [make_chunk("c2")], [[0.0] * DIMENSIONS], [])
        assert len(existing["chunks"]) == original_len

    def test_result_has_index_metadata(self):
        existing = make_index(chunks=[])
        result = merge_embeddings(existing, [], [], [])
        assert result["version"] == INDEX_VERSION
        assert result["model"] == MODEL_NAME


# ===================================================================
# TestSearchChunks
# ===================================================================

class TestSearchChunks:
    def _vec(self, val):
        """Return a deterministic embedding with one non-zero component."""
        v = [0.0] * DIMENSIONS
        v[0] = val
        return v

    def test_end_to_end_filter_and_rank(self):
        idx = make_index(chunks=[
            make_chunk("c1", agents=["Worker"], embedding=self._vec(0.9)),
            make_chunk("c2", agents=["Worker"], embedding=self._vec(0.1)),
            make_chunk("c3", agents=["Reviewer"], embedding=self._vec(0.5)),
        ])
        result = search_chunks(idx, self._vec(1.0), "Worker", None, 5)
        assert len(result) == 2  # c3 excluded (agent=Reviewer, no "all")
        assert result[0]["id"] == "c1"

    def test_no_filters_searches_all_chunks(self):
        idx = make_index(chunks=[
            make_chunk("c1", embedding=self._vec(0.9)),
            make_chunk("c2", embedding=self._vec(0.1)),
        ])
        result = search_chunks(idx, self._vec(1.0), None, None, 10)
        assert len(result) == 2

    def test_agent_filter_applied_before_ranking(self):
        idx = make_index(chunks=[
            make_chunk("c1", agents=["Debug"], embedding=self._vec(0.9)),
            make_chunk("c2", agents=["Worker"], embedding=self._vec(0.1)),
        ])
        result = search_chunks(idx, self._vec(1.0), "Worker", None, 10)
        ids = [c["id"] for c in result]
        assert "c1" not in ids

    def test_tech_filter_applied_before_ranking(self):
        idx = make_index(chunks=[
            make_chunk("c1", technologies=["python"], embedding=self._vec(0.9)),
            make_chunk("c2", technologies=["go"], embedding=self._vec(0.5)),
        ])
        result = search_chunks(idx, self._vec(1.0), None, "python", 10)
        ids = [c["id"] for c in result]
        assert "c2" not in ids

    def test_combined_filters(self):
        idx = make_index(chunks=[
            make_chunk("c1", agents=["Worker"], technologies=["python"], embedding=self._vec(0.9)),
            make_chunk("c2", agents=["Worker"], technologies=["go"], embedding=self._vec(0.8)),
            make_chunk("c3", agents=["Debug"], technologies=["python"], embedding=self._vec(0.7)),
        ])
        result = search_chunks(idx, self._vec(1.0), "Worker", "python", 10)
        ids = [c["id"] for c in result]
        assert ids == ["c1"]

    def test_no_matches_after_filtering_returns_empty(self):
        idx = make_index(chunks=[
            make_chunk("c1", agents=["Debug"], technologies=["go"]),
        ])
        result = search_chunks(idx, self._vec(1.0), "Worker", "python", 10)
        assert result == []

    def test_top_k_respected(self):
        idx = make_index(chunks=[
            make_chunk("c1", embedding=self._vec(0.9)),
            make_chunk("c2", embedding=self._vec(0.8)),
            make_chunk("c3", embedding=self._vec(0.7)),
        ])
        result = search_chunks(idx, self._vec(1.0), None, None, 2)
        assert len(result) == 2

    def test_results_have_score_key(self):
        idx = make_index(chunks=[make_chunk("c1", embedding=self._vec(0.5))])
        result = search_chunks(idx, self._vec(1.0), None, None, 5)
        assert "score" in result[0]
        assert result[0]["score"] == pytest.approx(0.5)
