"""Tests for src.utils.playbook_parser — TDD red phase."""

import hashlib
import os

import pytest

from src.utils.playbook_parser import (
    REQUIRED_FIELDS,
    VALID_CATEGORIES,
    _compute_content_hash,
    _extract_frontmatter,
    _validate_content,
    _validate_frontmatter,
    _validate_unique_ids,
    discover_playbook_files,
    parse_all_playbooks,
    parse_playbook_file,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

VALID_PLAYBOOK = '''\
+++
id = "shared/test-rule"
title = "Test Rule"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["test"]
version = 1
+++

### Test Rule

This is a test rule for unit testing purposes.
'''

VALID_META = {
    "id": "shared/test-rule",
    "title": "Test Rule",
    "agents": ["all"],
    "technologies": ["all"],
    "category": "rule",
    "tags": ["test"],
    "version": 1,
}


def _make_playbook(tmp_path, name="test.playbook.md", content=VALID_PLAYBOOK):
    """Write a playbook file and return its path."""
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


# ===================================================================
# _extract_frontmatter
# ===================================================================


class TestExtractFrontmatter:
    """Tests for _extract_frontmatter."""

    def test_valid_toml_parses(self):
        meta, body = _extract_frontmatter(VALID_PLAYBOOK)
        assert meta["id"] == "shared/test-rule"

    def test_returns_correct_body(self):
        _, body = _extract_frontmatter(VALID_PLAYBOOK)
        assert "### Test Rule" in body

    def test_multiple_frontmatter_fields(self):
        meta, _ = _extract_frontmatter(VALID_PLAYBOOK)
        assert isinstance(meta["agents"], list)
        assert isinstance(meta["version"], int)
        assert isinstance(meta["title"], str)

    def test_body_with_markdown_content(self):
        _, body = _extract_frontmatter(VALID_PLAYBOOK)
        assert "unit testing purposes" in body

    def test_missing_opening_delimiter_raises(self):
        raw = 'id = "x"\n+++\nBody'
        with pytest.raises(ValueError, match="frontmatter"):
            _extract_frontmatter(raw)

    def test_missing_closing_delimiter_raises(self):
        raw = '+++\nid = "x"\nBody without closing'
        with pytest.raises(ValueError, match="frontmatter"):
            _extract_frontmatter(raw)

    def test_empty_frontmatter_section(self):
        raw = "+++\n\n+++\nBody here"
        meta, body = _extract_frontmatter(raw)
        assert meta == {}
        assert "Body here" in body

    def test_malformed_toml_raises(self):
        raw = '+++\nid = [unclosed\n+++\nBody'
        with pytest.raises(ValueError, match="Malformed TOML"):
            _extract_frontmatter(raw)

    def test_special_characters_in_values(self):
        raw = '+++\nid = "rule/special-chars_v2"\ntitle = "Héllo — World"\nagents = ["all"]\n+++\nBody'
        meta, _ = _extract_frontmatter(raw)
        assert meta["title"] == "Héllo — World"

    def test_body_with_triple_plus_inline(self):
        raw = '+++\nid = "x"\n+++\nSome text with +++ in the middle\n'
        meta, body = _extract_frontmatter(raw)
        assert "+++ in the middle" in body

    def test_windows_line_endings(self):
        raw = "+++\r\nid = \"win\"\r\n+++\r\nBody\r\n"
        meta, body = _extract_frontmatter(raw)
        assert meta["id"] == "win"
        assert "Body" in body

    def test_no_frontmatter_at_all_raises(self):
        raw = "Just a body with no frontmatter at all"
        with pytest.raises(ValueError, match="frontmatter"):
            _extract_frontmatter(raw)

    def test_only_opening_delimiter_raises(self):
        raw = "+++\nsome TOML\nand body"
        with pytest.raises(ValueError, match="frontmatter"):
            _extract_frontmatter(raw)

    def test_toml_with_multiline_string(self):
        raw = '+++\nid = "multi"\ntitle = "Hello"\nagents = ["a", "b"]\n+++\nBody'
        meta, _ = _extract_frontmatter(raw)
        assert meta["agents"] == ["a", "b"]

    def test_returns_tuple(self):
        result = _extract_frontmatter(VALID_PLAYBOOK)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_body_preserves_leading_newline(self):
        _, body = _extract_frontmatter(VALID_PLAYBOOK)
        assert body.startswith("\n")


# ===================================================================
# _validate_frontmatter
# ===================================================================


class TestValidateFrontmatter:
    """Tests for _validate_frontmatter."""

    def test_valid_frontmatter_passes(self):
        _validate_frontmatter(VALID_META, "test.md")

    def test_missing_id_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "id"}
        with pytest.raises(ValueError, match="id"):
            _validate_frontmatter(meta, "test.md")

    def test_missing_title_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "title"}
        with pytest.raises(ValueError, match="title"):
            _validate_frontmatter(meta, "test.md")

    def test_missing_agents_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "agents"}
        with pytest.raises(ValueError, match="agents"):
            _validate_frontmatter(meta, "test.md")

    def test_missing_technologies_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "technologies"}
        with pytest.raises(ValueError, match="technologies"):
            _validate_frontmatter(meta, "test.md")

    def test_missing_category_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "category"}
        with pytest.raises(ValueError, match="category"):
            _validate_frontmatter(meta, "test.md")

    def test_missing_tags_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "tags"}
        with pytest.raises(ValueError, match="tags"):
            _validate_frontmatter(meta, "test.md")

    def test_missing_version_raises(self):
        meta = {k: v for k, v in VALID_META.items() if k != "version"}
        with pytest.raises(ValueError, match="version"):
            _validate_frontmatter(meta, "test.md")

    def test_invalid_category_value_raises(self):
        meta = {**VALID_META, "category": "nonsense"}
        with pytest.raises(ValueError, match="Invalid category"):
            _validate_frontmatter(meta, "test.md")

    def test_agents_not_list_raises(self):
        meta = {**VALID_META, "agents": "all"}
        with pytest.raises(ValueError, match="agents.*list"):
            _validate_frontmatter(meta, "test.md")

    def test_technologies_not_list_raises(self):
        meta = {**VALID_META, "technologies": "python"}
        with pytest.raises(ValueError, match="technologies.*list"):
            _validate_frontmatter(meta, "test.md")

    def test_tags_not_list_raises(self):
        meta = {**VALID_META, "tags": "test"}
        with pytest.raises(ValueError, match="tags.*list"):
            _validate_frontmatter(meta, "test.md")

    def test_version_not_int_raises(self):
        meta = {**VALID_META, "version": "1"}
        with pytest.raises(ValueError, match="version.*int"):
            _validate_frontmatter(meta, "test.md")

    def test_empty_agents_list_is_ok(self):
        meta = {**VALID_META, "agents": []}
        _validate_frontmatter(meta, "test.md")

    def test_error_message_includes_filepath(self):
        meta = {k: v for k, v in VALID_META.items() if k != "id"}
        with pytest.raises(ValueError, match="my/file.md"):
            _validate_frontmatter(meta, "my/file.md")

    def test_all_valid_categories_accepted(self):
        for cat in VALID_CATEGORIES:
            meta = {**VALID_META, "category": cat}
            _validate_frontmatter(meta, "test.md")

    def test_version_float_raises(self):
        meta = {**VALID_META, "version": 1.5}
        with pytest.raises(ValueError, match="version.*int"):
            _validate_frontmatter(meta, "test.md")


# ===================================================================
# _validate_content
# ===================================================================


class TestValidateContent:
    """Tests for _validate_content."""

    def test_valid_body_passes(self):
        _validate_content("### Heading\n\nSome content.", "f.md")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="Empty playbook body"):
            _validate_content("", "f.md")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="Empty playbook body"):
            _validate_content("   \t  ", "f.md")

    def test_newlines_only_raises(self):
        with pytest.raises(ValueError, match="Empty playbook body"):
            _validate_content("\n\n\n", "f.md")

    def test_error_includes_filepath(self):
        with pytest.raises(ValueError, match="my/path.md"):
            _validate_content("", "my/path.md")

    def test_single_word_passes(self):
        _validate_content("word", "f.md")


# ===================================================================
# _compute_content_hash
# ===================================================================


class TestComputeContentHash:
    """Tests for _compute_content_hash."""

    def test_deterministic(self):
        h1 = _compute_content_hash("hello world")
        h2 = _compute_content_hash("hello world")
        assert h1 == h2

    def test_different_input_different_hash(self):
        h1 = _compute_content_hash("hello")
        h2 = _compute_content_hash("world")
        assert h1 != h2

    def test_crlf_normalized_to_lf(self):
        h1 = _compute_content_hash("line1\r\nline2")
        h2 = _compute_content_hash("line1\nline2")
        assert h1 == h2

    def test_leading_trailing_whitespace_stripped(self):
        h1 = _compute_content_hash("  hello  ")
        h2 = _compute_content_hash("hello")
        assert h1 == h2

    def test_sha256_prefix(self):
        h = _compute_content_hash("test")
        assert h.startswith("sha256:")

    def test_hex_digest_length(self):
        h = _compute_content_hash("test")
        hex_part = h.removeprefix("sha256:")
        assert len(hex_part) == 64

    def test_known_hash_value(self):
        content = "test"
        expected = hashlib.sha256(b"test").hexdigest()
        assert _compute_content_hash(content) == f"sha256:{expected}"


# ===================================================================
# _validate_unique_ids
# ===================================================================


class TestValidateUniqueIds:
    """Tests for _validate_unique_ids."""

    def test_unique_ids_pass(self):
        chunks = [
            {"id": "a", "source_file": "f1.md"},
            {"id": "b", "source_file": "f2.md"},
        ]
        _validate_unique_ids(chunks)

    def test_duplicate_ids_raise(self):
        chunks = [
            {"id": "a", "source_file": "f1.md"},
            {"id": "a", "source_file": "f2.md"},
        ]
        with pytest.raises(ValueError, match="Duplicate id 'a'"):
            _validate_unique_ids(chunks)

    def test_duplicate_error_mentions_both_files(self):
        chunks = [
            {"id": "x", "source_file": "first.md"},
            {"id": "x", "source_file": "second.md"},
        ]
        with pytest.raises(ValueError, match="first.md"):
            _validate_unique_ids(chunks)

    def test_single_chunk_passes(self):
        _validate_unique_ids([{"id": "only", "source_file": "f.md"}])

    def test_empty_list_passes(self):
        _validate_unique_ids([])

    def test_many_unique_ids(self):
        chunks = [{"id": f"id-{i}", "source_file": f"f{i}.md"} for i in range(100)]
        _validate_unique_ids(chunks)


# ===================================================================
# parse_playbook_file
# ===================================================================


class TestParsePlaybookFile:
    """Tests for parse_playbook_file."""

    def test_valid_file_parses(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert result["id"] == "shared/test-rule"

    def test_returns_all_expected_keys(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        expected_keys = {
            "id", "title", "agents", "technologies", "category",
            "tags", "version", "content", "content_hash", "source_file",
        }
        assert set(result.keys()) == expected_keys

    def test_content_hash_present(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert result["content_hash"].startswith("sha256:")

    def test_source_file_matches_input(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert result["source_file"] == p

    def test_content_stripped(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert not result["content"].startswith("\n")

    def test_malformed_toml_raises(self, tmp_path):
        bad = "+++\nid = [broken\n+++\nBody"
        p = _make_playbook(tmp_path, content=bad)
        with pytest.raises(ValueError, match="Malformed TOML"):
            parse_playbook_file(p)

    def test_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            parse_playbook_file("/no/such/file.playbook.md")

    def test_empty_body_raises(self, tmp_path):
        pb = '+++\nid = "x"\ntitle = "T"\nagents = ["a"]\ntechnologies = ["a"]\ncategory = "rule"\ntags = ["t"]\nversion = 1\n+++\n   \n'
        p = _make_playbook(tmp_path, content=pb)
        with pytest.raises(ValueError, match="Empty playbook body"):
            parse_playbook_file(p)

    def test_missing_field_raises(self, tmp_path):
        pb = '+++\nid = "x"\ntitle = "T"\n+++\nBody here'
        p = _make_playbook(tmp_path, content=pb)
        with pytest.raises(ValueError, match="Missing required field"):
            parse_playbook_file(p)

    def test_agents_value(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert result["agents"] == ["all"]

    def test_version_value(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert result["version"] == 1

    def test_tags_value(self, tmp_path):
        p = _make_playbook(tmp_path)
        result = parse_playbook_file(p)
        assert result["tags"] == ["test"]


# ===================================================================
# discover_playbook_files
# ===================================================================


class TestDiscoverPlaybookFiles:
    """Tests for discover_playbook_files."""

    def test_finds_files_in_nested_dirs(self, tmp_path):
        sub = tmp_path / "a" / "b"
        sub.mkdir(parents=True)
        (sub / "deep.playbook.md").write_text(VALID_PLAYBOOK, encoding="utf-8")
        result = discover_playbook_files(str(tmp_path))
        assert len(result) == 1
        assert result[0].endswith("deep.playbook.md")

    def test_skips_underscore_prefixed(self, tmp_path):
        (tmp_path / "_template.playbook.md").write_text("x", encoding="utf-8")
        (tmp_path / "real.playbook.md").write_text("x", encoding="utf-8")
        result = discover_playbook_files(str(tmp_path))
        assert len(result) == 1
        assert "real.playbook.md" in result[0]

    def test_returns_sorted_absolute_paths(self, tmp_path):
        (tmp_path / "b.playbook.md").write_text("x", encoding="utf-8")
        (tmp_path / "a.playbook.md").write_text("x", encoding="utf-8")
        result = discover_playbook_files(str(tmp_path))
        assert result == sorted(result)
        assert all(os.path.isabs(p) for p in result)

    def test_empty_directory_returns_empty(self, tmp_path):
        result = discover_playbook_files(str(tmp_path))
        assert result == []

    def test_non_playbook_files_ignored(self, tmp_path):
        (tmp_path / "readme.md").write_text("x", encoding="utf-8")
        (tmp_path / "code.py").write_text("x", encoding="utf-8")
        result = discover_playbook_files(str(tmp_path))
        assert result == []

    def test_multiple_files_found(self, tmp_path):
        (tmp_path / "one.playbook.md").write_text("x", encoding="utf-8")
        (tmp_path / "two.playbook.md").write_text("x", encoding="utf-8")
        result = discover_playbook_files(str(tmp_path))
        assert len(result) == 2


# ===================================================================
# parse_all_playbooks
# ===================================================================


class TestParseAllPlaybooks:
    """Tests for parse_all_playbooks."""

    def _make_valid(self, tmp_path, name, pb_id):
        content = f'+++\nid = "{pb_id}"\ntitle = "T"\nagents = ["a"]\ntechnologies = ["a"]\ncategory = "rule"\ntags = ["t"]\nversion = 1\n+++\n\n### Body\n\nContent.\n'
        (tmp_path / name).write_text(content, encoding="utf-8")

    def test_multiple_valid_files_parsed(self, tmp_path):
        self._make_valid(tmp_path, "a.playbook.md", "id-a")
        self._make_valid(tmp_path, "b.playbook.md", "id-b")
        result = parse_all_playbooks(str(tmp_path))
        assert len(result) == 2

    def test_duplicate_ids_across_files_raises(self, tmp_path):
        self._make_valid(tmp_path, "a.playbook.md", "same-id")
        self._make_valid(tmp_path, "b.playbook.md", "same-id")
        with pytest.raises(ValueError, match="Duplicate id"):
            parse_all_playbooks(str(tmp_path))

    def test_empty_directory_returns_empty(self, tmp_path):
        result = parse_all_playbooks(str(tmp_path))
        assert result == []

    def test_results_contain_expected_keys(self, tmp_path):
        self._make_valid(tmp_path, "x.playbook.md", "id-x")
        result = parse_all_playbooks(str(tmp_path))
        assert "content_hash" in result[0]
        assert "source_file" in result[0]

    def test_skips_underscore_files(self, tmp_path):
        self._make_valid(tmp_path, "_skip.playbook.md", "skip")
        self._make_valid(tmp_path, "keep.playbook.md", "keep")
        result = parse_all_playbooks(str(tmp_path))
        assert len(result) == 1
        assert result[0]["id"] == "keep"


# ---------------------------------------------------------------------------
# Integration: validate ALL repo playbooks parse correctly
# ---------------------------------------------------------------------------

REPO_PLAYBOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "playbooks")


@pytest.mark.skipif(
    not os.path.isdir(REPO_PLAYBOOK_DIR),
    reason="docs/playbooks/ not found (running outside repo root)",
)
class TestRepoPlaybooksIntegration:
    """Verify every .playbook.md in the repo parses without error."""

    def test_all_repo_playbooks_parse(self):
        chunks = parse_all_playbooks(REPO_PLAYBOOK_DIR)
        assert len(chunks) > 0, "Expected at least one playbook in docs/playbooks/"

    def test_no_duplicate_ids_in_repo(self):
        chunks = parse_all_playbooks(REPO_PLAYBOOK_DIR)
        ids = [c["id"] for c in chunks]
        assert len(ids) == len(set(ids)), f"Duplicate IDs found: {[i for i in ids if ids.count(i) > 1]}"
