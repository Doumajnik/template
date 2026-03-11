+++
id = "agents/scaffolder"
title = "Scaffolder Agent Rules"
agents = ["scaffolder"]
technologies = ["all"]
category = "rule"
tags = ["scaffolder"]
version = 2
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
