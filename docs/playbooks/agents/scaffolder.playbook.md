+++
id = "agents/scaffolder"
title = "Scaffolder Agent Rules"
agents = ["scaffolder"]
technologies = ["all"]
category = "rule"
tags = ["scaffolder"]
version = 4
+++

### Scaffolder Guidelines

- Create file stubs with function signatures, type annotations, and docstrings — NO implementation logic
- Implementation bodies must be `raise NotImplementedError("...")` or equivalent — never real code
- Follow the directory structure from the plan: `src/utils/`, `src/services/`, `src/models/`, `src/config/`
- Test files must mirror source structure: `src/utils/foo.py` → `tests/utils/test_foo.py`
- Include all necessary imports in stubs — the file should be syntactically valid
- Use the exact function names and signatures from the architecture plan — don't rename or reinterpret
- Create `__init__.py` files for all Python packages to ensure proper imports
- Add module-level docstrings describing the file's purpose and responsibility
- If the plan specifies interfaces/protocols, scaffold those first — implementations depend on them
- Check `docs/CODE_INVENTORY.md` to avoid creating files that duplicate existing functionality
- Mark all scaffolding tasks as ✅ complete in the todo file after creation
- Define `__all__` in `__init__.py` files to explicitly control the public API of each package — only export symbols that other packages should use (source: Python docs, "Importing * From a Package")
- Use absolute imports in all stubs — avoid relative imports unless referencing sibling modules within the same subpackage (source: Python docs, PEP 8)
- Place shared type aliases and type definitions in a dedicated `types.py` or `models.py` at the package level — avoid scattering type definitions across unrelated modules
- Group imports in stubs following PEP 8 order: standard library, blank line, third-party, blank line, local application — each group alphabetically sorted
- For packages with subpackages, scaffold the dependency tree bottom-up — create leaf modules first, then modules that import from them, to ensure valid imports at every stage
- Every stub file must be syntactically valid and importable — run a syntax check (`python -c "import module"`) before marking scaffolding complete
- Prevent circular imports by enforcing a strict dependency direction — lower-level modules (models, utils) must never import from higher-level modules (services, handlers); draw the import graph as a DAG before scaffolding (source: Python docs, "The import system", section 5.3)
- Use lazy imports (inside functions) for heavy or optional dependencies that are expensive to load at module level — this speeds up startup and avoids circular import chains (source: Python docs, PEP 690)
- Use `TYPE_CHECKING` guards for type-only imports — wrap imports used solely for type annotations in `if TYPE_CHECKING:` blocks to break circular dependencies at runtime while preserving static analysis (source: Python docs, typing module)
- Keep `__init__.py` files lightweight — never perform heavy computation, I/O, or complex initialization in `__init__.py`; it executes on every import of the package or any submodule (source: Python docs, "Regular packages", section 5.2.1)
- Ensure every scaffolded module is importable in isolation — no module should fail to import when its dependencies are available, even if the rest of the application is not loaded (source: Python docs, "The module cache", section 5.3.1)
- Avoid wildcard imports (`from module import *`) in all stubs — they pollute the namespace, make dependencies opaque, and complicate static analysis (source: Python docs, PEP 8)
