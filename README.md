# flawpath

**50 validated backend implementation skills**, plus a `flawplan` CLI that turns a handler inventory into a phase-ordered assessment plan.

Authorized testing only: every skill describes how to *map, probe, confirm, harden and report* implementation behaviour in APIs you own or have written permission to test. The corpus contains no weaponized payload and no live target data.

```shell
python -m pip install -e ".[dev]"
flawpath validate          # -> flawpath: 50/50 skills valid
flawpath build             # -> skills/, pack.json, results/
python -m pytest -q        # -> 23 passed
```

## Why this pack exists

Backend implementation defects are found by reading, not by scanning, and the reading is never written down: which fields the parser passes through, whether validation runs before or after construction, what an omitted field does during a partial update, whether two parsers apply different policies to the same bytes, and which error shape came from which layer. Each assessment re-derives that map from scratch, and the probe that found something cannot be replayed by anyone else because the map lived in one person's head.

`flawpath` makes it checkable. Each of the 50 skills is one self-contained procedure with a stated **use when** and **avoid when**, a numbered procedure, observable **signals**, concrete **patterns**, known **pitfalls** and **done when** criteria. A validator enforces the floor on all of them and the CLI will not report success below 50/50.

## The arc

| Phase | Count | What it covers |
|---|---|---|
| `scope` | 7 | assessment boundary, route inventory, write surface and state map, environment delta, synthetic records, mutation budget and rollback, observability ownership |
| `map` | 8 | route-verb matrix, parameter provenance, parse/validate order, identifier shape, middleware chain, response field exposure, error surface, integration and async triggers |
| `probe` | 19 | unknown and privileged fields, nested keys, coercion, defaults, batch scope, filters, pagination and search reach, error disclosure, debug routes, content type, duplicate keys, partial-update omission, enum boundaries, concurrency, idempotency, rate limits, cache invalidation |
| `confirm` | 6 | clean-state reproduction, single-input attribution, response differential, precondition and effect, environment transferability, ruling out alternatives |
| `harden` | 6 | server-side field allowlist, strict DTO boundary, uniform errors, debug surface disabled, concurrency guard and idempotency, regression probe suite |
| `document` | 4 | evidence pack, reproduction in client terms, fixes worded in framework terms, coordinated retest and closure |

## CLI

```shell
flawpath validate --json               # the 50/50 gate, machine-readable
flawpath list --phase probe            # 19 skills
flawpath show unknown-field-acceptance
flawpath search field validation
flawpath build                         # regenerate skills/, pack.json, results/
flawpath flawplan --inventory-file examples/demo-inventory.json
```

### `flawplan`

`flawplan` is this pack's domain command. It reads a small JSON inventory of what the API actually is —

```json
{
  "target": "orders service",
  "framework": "express-style router with a body parser middleware",
  "routes": ["/api/v1/orders", "/api/v1/orders/:id"],
  "parameters": ["path", "query", "body", "header", "cookie"],
  "auth_model": ["member", "billing-service"],
  "observed": { "unknown_field_policy": "pass through", "validation_stage": "after construction" },
  "concerns": ["can a client set a field the role matrix reserves"]
}
```

— flattens it into vocabulary (including the *names* of observed settings, since `unknown_field_policy` describes the receiver as much as its value does), scores every skill against that vocabulary, and emits a plan in phase order. Selection is **phase-stratified**: the first pass takes the best match in each matched phase before any phase gets a second slot, so a small `--top` can never crowd out the later phases of the arc. *Thin coverage* lists phases the inventory matched nothing in, computed from matches rather than from the truncated plan.

## Layout

```text
src/flawpath/
├─ corpus/        authored skill data — the single source of truth
│  ├─ part1.py    skills 1-15   (scope, map)
│  ├─ part2.py    skills 16-34  (probe)
│  └─ part3.py    skills 35-50  (confirm, harden, document)
├─ model.py       Skill dataclass + strict dict loading
├─ render.py      deterministic SKILL.md / pack.json / results writer
├─ validate.py    every rule, one place
└─ cli.py         validate / list / show / search / build / flawplan
```

Markdown under `skills/` is **generated**. Edit the corpus, run `flawpath build`, and a test asserts the committed files match a fresh render — the two can never silently disagree.

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — components, data flow, design decisions
- [docs/USAGE.md](docs/USAGE.md) — commands, agent integration, regeneration discipline
- [docs/PROJECT_SPEC.md](docs/PROJECT_SPEC.md) — problem, solution, acceptance tests
- [RESULTS.md](RESULTS.md) — reproducible evidence for every claim above
- [SECURITY.md](SECURITY.md) — authorized-use scope and the reporting path
- [CONTRIBUTING.md](CONTRIBUTING.md) — the quality floor CI enforces

## License

MIT. References link to public specifications and guidance; see each skill's **References** section.