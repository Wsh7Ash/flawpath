# Results

Reproducible evidence for the claims in `README.md`.

## Environment

- OS: Windows (MSYS2 shell)
- Python: 3.14.3 (`requires-python >= 3.10`)
- Runtime dependencies: none (standard library only)
- Dev dependency: `pytest`
- Network: none required at any point — the package performs no network requests

## Validation performed

### 1. Corpus gate — PASS

```shell
$ PYTHONPATH=src python -m flawpath validate
flawpath: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Exit code 0. With generated files included (the default), this also byte-compares every `skills/**/SKILL.md` against a fresh render.

### 2. Test suite — PASS (23 tests)

```shell
$ PYTHONPATH=src python -m pytest -q
.......................                                                  [100%]
23 passed
```

Covered: pack declares and delivers 50; slugs and titles unique; every skill passes every rule; all six phases populated and balanced; word floor holds on the weakest skill; no placeholder or machine-local path tokens; **no live credential or private address anywhere in the corpus**; **`scope` and `map` provably precede `probe` in `PHASE_ORDER`**; committed `SKILL.md` files match the render; `pack.json` hashes match file bytes; build is byte-idempotent in a temp directory; drift is detected; `validate --json` reports 50/50; `list`/`show`/`search` behave as documented; `flawplan` orders phases, covers all six with `--top 12` and with `--top 6`, rejects a missing inventory, reports every phase as thin coverage for an inventory that matches nothing, and aggregates vocabulary across inventory keys (including nested key names); `results/validation.json` and `results/catalog.md` are consistent with the corpus.

### 3. Build and artifact sync — PASS

```shell
$ PYTHONPATH=src python -m flawpath build
built 50 skills -> .../flawpath/skills
$ PYTHONPATH=src python -m flawpath validate
flawpath: 50/50 skills valid
```

Regenerating twice produces byte-identical output; `test_build_is_idempotent` asserts this against a clean temp directory.

### 4. Phase distribution — as specified

| Phase | Skills |
|---|---|
| scope | 7 |
| map | 8 |
| probe | 19 |
| confirm | 6 |
| harden | 6 |
| document | 4 |
| **total** | **50** |

`flawpath list --phase probe` returns 19; every other phase filter returns its count above.

### 5. `flawplan` on the checked-in example — PASS

```shell
$ PYTHONPATH=src python -m flawpath flawplan --inventory-file examples/demo-inventory.json
# Assessment plan - orders service
Framework: express-style router with a body parser middleware   Routes: 3   Parameters: 5   Skills matched: 50 of 50   Plan steps: 12   Phases covered: 6/6

Routes: /api/v1/orders, /api/v1/orders/:id, /internal/reindex
Parameter sources: path, query, body, header, cookie

## scope
...
```

Observed behaviour: 50 of 50 skills matched the inventory vocabulary; the plan contains 12 steps spread across **all 6 phases** despite `--top 12`; `missing_phases` is empty because every phase matched. With `--top 6` the plan still covers 6/6 phases.

For an inventory whose vocabulary matches nothing (`{"keywords": ["qqqqqq", "zzzzzz"]}`), `skills_matched` is 0, `plan_steps` is 0 and `missing_phases` lists all six phases — confirming thin coverage is derived from matches rather than from the truncated plan.

### 6. Cross-pack uniqueness — PASS

Against sibling packs `edgescout` (50) and `hookproof` (50): **0 slug overlap, 0 title overlap** across all three corpora.

## Commands executed

```shell
python -m flawpath validate --json
python -m flawpath validate
python -m flawpath build
python -m flawpath list --phase probe
python -m flawpath search field validation
python -m flawpath flawplan --inventory-file examples/demo-inventory.json
python -m pytest -q
```

## Known limitations

- **`flawplan` is vocabulary matching, not an assessment engine.** It scores observed tokens against skill text. It will not tell you which route matters most, only which skills relate to the inventory you described and which phases you matched nothing in.
- **Thin coverage is only as good as the inventory.** An inventory that omits a parameter source or an auth role will not surface the phase for it.
- **The pack does not send requests.** Nothing here contacts an API, mutates a record or reads your source tree. Every mapping and probe still has to be executed by the tester under the boundary they established.
- **Attribution requires the tester.** `single-input-attribution` tells you how to isolate a cause; it cannot isolate it for you.
- Tests were run on Python 3.14 locally. CI additionally covers 3.10, 3.12 and 3.13.

## Generated artifacts

| Path | What it is |
|---|---|
| `skills/**/SKILL.md` | 50 rendered skills, byte-identical to the corpus |
| `pack.json` | manifest with SHA-256 per skill file |
| `results/catalog.md` | generated skill catalog table |
| `results/validation.json` | machine-readable gate report (`passed: true`) |
| `examples/demo-inventory.json` | the example inventory used above |