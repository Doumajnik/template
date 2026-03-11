+++
id = "technologies/python"
title = "Python Conventions"
agents = []
technologies = ["python"]
category = "convention"
tags = ["python", "stdlib", "typing"]
version = 3
+++

### Python Conventions

- Use Python 3 features everywhere: f-strings, type hints, `pathlib`, `dataclasses`. No Python 2 compatibility code
- Add type annotations on all public function signatures. Use `collections.abc` for generic types (`Sequence`, `Mapping`) — not `typing.List` or `typing.Dict`
- Use absolute imports only. Group imports in order: stdlib → third-party → local, separated by a single blank line
- No wildcard imports (`from x import *`). Import specific names or use the module namespace
- Prefer f-strings for string formatting. Do not use `.format()` or `%` formatting
- Use `pathlib.Path` for all file path operations — never string concatenation or `os.path.join()`
- Use `dataclasses.dataclass` or `typing.NamedTuple` for structured data containers — avoid plain dicts for data with a known shape
- Catch specific exceptions. Never use bare `except:` or `except Exception:` without re-raising. Always include context in error messages
- Use context managers (`with` statement) for files, locks, database connections, and any resource that needs cleanup
- Use list comprehensions for simple one-level transformations only. No nested comprehensions. Use a loop with `append` for complex or multi-step logic
- Use `enum.Enum` for fixed sets of related constants instead of module-level string/int constants
- Write Google-style docstrings on all public functions with `Args:`, `Returns:`, and `Raises:` sections
- Testing: use `pytest` with `@pytest.mark.parametrize` for data-driven tests. Use fixtures for setup/teardown, not `setUp`/`tearDown` methods
- Define `__all__` in any module that has a public API to explicitly control what is exported
- Use `isinstance()` for type checking — never compare with `type()`. Check against abstract base classes when possible
- Use the `logging` module for all production output. Never use `print()` in production code
- Always use virtual environments (`venv` or similar). Never install packages globally or with `--user` in CI
- Use `functools.lru_cache` or `functools.cache` for memoizing expensive pure functions
- Use `typing.Protocol` for structural subtyping instead of ABC when you only need method signatures
- Use `contextlib.suppress` for ignoring specific exceptions cleanly — not try/except/pass
- Prefer `collections.defaultdict` over manual dict key initialization
- Use `itertools` for lazy iteration patterns — `chain`, `islice`, `groupby` — avoid materializing large lists
- Use `textwrap.dedent` for multi-line string constants to keep code indentation clean
- Use `@property` for computed attributes — never expose internal state directly
- Use `__slots__` on data-heavy classes to reduce memory usage
- Prefer `str.removeprefix()` and `str.removesuffix()` (3.9+) over manual slicing
- Use `tomllib` (3.11+) for reading TOML — never parse config manually
- Pin all dependencies in `requirements.txt` with exact versions. Use `pip-compile` for reproducible builds
- Use `argparse` for CLI tools — never `sys.argv` parsing
- Prefer `json.loads`/`json.dumps` with explicit `encoding='utf-8'` for file operations
- Use `unittest.mock.patch` as a decorator or context manager — never monkeypatch globals directly
