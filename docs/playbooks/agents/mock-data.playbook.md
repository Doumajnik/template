+++
id = "agents/mock-data"
title = "Mock Data Generator Agent Rules"
agents = ["mock-data"]
technologies = ["all"]
category = "rule"
tags = ["mock-data", "fixtures", "testing"]
version = 1
+++

### Mock Data Generator Guidelines

- **Single source of truth.** Every domain entity has exactly one factory/builder under `tests/fixtures/`. Tests import the factory; they never copy-paste fixture dicts.
- **Realistic defaults.** No `John Doe`, no `1970-01-01`, no `100.00`. Names from varied locales, dates spanning realistic ranges, amounts from realistic distributions.
- **Locale-aware by default.** At least 10% of string fields produce UTF-8 / RTL / emoji / accented characters out of the box.
- **Adversarial defaults included.** Every builder offers a variant or override with very-long strings, unicode-heavy strings, NULL bytes, leading/trailing whitespace, NaN/Inf, RTL — to surface latent bugs in normalisation, length checks, and encoding.
- **Deterministic.** Every random choice goes through a seeded RNG. The same seed produces the same fixture across runs.
- **Schema-validated.** Every fixture is validated against its declared schema (Pydantic / zod / JSON Schema). A fixture that does not validate is rejected.
- **Cross-entity consistency.** Foreign keys, ownership, and relational constraints are honoured by default — a `User`'s `Order`s actually reference that user.
- **Append seeds, never overwrite.** `tests/fixtures/seeds/{scenario}.json` files are tracked in git and stable; new scenarios get new files.
- **Document every fixture.** `tests/fixtures/README.md` lists every factory + seed with the entity it covers, scenarios that use it, and the schema it validates against.
- **No production data.** Never copy real customer data — even anonymised. Always synthesise.
- **Contract payloads cover happy path + every documented error + edge cases.** Skipping the error path means contract tests don't catch error-shape drift.
- **Outputs are write-only into `tests/fixtures/`.** Mock Data never modifies `src/` or `tests/` outside the fixtures directory.
