# Architecture

## Goals

1. **One source of truth.** Skills are authored as Python data; Markdown files are generated. A test asserts committed files match a fresh render, so the two can never disagree.
2. **Validation is a first-class gate.** Every quality floor lives in `validate.py` and is enforced by both the CLI and the test suite.
3. **No runtime dependencies.** Standard library only, so the pack runs anywhere Python 3.10+ exists.

## Components

```text
src/flawpath/
├─ corpus/           authored skill data (source of truth)
│  ├─ __init__.py    PACK metadata, PHASE_ORDER + loads part1..part3
│  ├─ part1.py       skills 1-15   (scope, map)
│  ├─ part2.py       skills 16-34  (probe)
│  └─ part3.py       skills 35-50  (confirm, harden, document)
├─ model.py          Skill dataclass + strict dict loading
├─ render.py         deterministic SKILL.md + pack.json + results writer
├─ validate.py       every rule, one place
└─ cli.py            validate / list / show / search / build / flawplan
```

### Data flow

```text
part1..part3 (dicts)
      │  skill_from_dict()  -- shape check, rejects missing/empty fields
      ▼
   Skill (frozen dataclass)
      │
      ├─ validate_pack()  ─▶ Issue list ─▶ CLI exit code (0 only at 50/50)
      └─ render_skill()   ─▶ skills/<slug>/SKILL.md  (byte-deterministic)

inventory.json ─▶ inventory_vocabulary() ─▶ build_flawplan()
                                             │  phase-stratified selection
                                             ▼
                      phase-ordered plan + thin-coverage phase list
```

### The flawplan command

`flawplan` is flawpath's domain command and separates this pack from a document library. It consumes a small inventory of what the API *is* — routes, framework, parameter sources, auth model, objects, observed settings and free-text concerns — and flattens it into lowercase tokens. Dict keys count as vocabulary as well as values, because a setting named `unknown_field_policy` describes the receiver as much as the word `pass` does.

Every skill is scored by counting how many of those tokens appear in its slug, title, summary, tags and steps.

Selection is **phase-stratified**: matches are bucketed by phase, sorted by score, and drawn round-robin in `PHASE_ORDER`. Round 0 takes the best match from every matched phase, round 1 the second-best, and so on until `--top` is reached. Two consequences:

- a small `--top` (even `top=6`) still yields one step from every phase the inventory matched;
- ordering inside the output still follows the arc, so the plan reads scope → map → probe → confirm → harden → document.

`missing_phases` is computed from **matched** skills, not from the truncated plan. Reporting "no matched skill in these phases" for a phase that matched but was cut by `--top` would be a false statement — and this pack's `confirm` phase exists precisely to make claims checkable, so a tool that misreports its own coverage would contradict the corpus it ships.

### Design decisions

- **`scope` and `map` precede every probe.** `PHASE_ORDER` enforces the discipline: a plan that starts probing before it has a boundary and a parameter map has skipped the two steps that make a later finding defensible. `test_scope_phase_always_precedes_probes` asserts the ordering so it cannot drift.
- **Attribution is a phase, not an afterthought.** `confirm` contains `single-input-attribution` and `response-differential-comparison` because a probe that changed three inputs supports no causal claim. Making confirmation a phase rather than an inline habit is the pack's main structural bet.
- **Class and reach are separate axes** in `confirm`, and fixes are worded per *layer* in `document` — a remediation that says "add validation" without naming the object to change has told the implementer nothing.
- **Phases are data, not code.** `PHASE_ORDER` lives in `corpus/__init__.py` next to `PACK`, so renderer, validator, CLI and tests all read one tuple.
- **Generated files are never hand-edited.** `validate` byte-compares every `skills/**/SKILL.md` against a fresh render, which is why CI can run `build` followed by `git diff --exit-code`.
- **`meta` is open-ended.** `PACK["meta_keys"]` declares required meta fields; this pack requires `phase`.

## Test surface

`tests/test_corpus.py` covers corpus shape (counts, uniqueness, phase balance), every validation rule, regeneration equality, drift detection, the scope-before-probe ordering, absence of live credentials and private addresses, every CLI subcommand including `flawplan`'s stratified selection and thin-coverage semantics, and the integrity of the committed `pack.json` hashes and `results/` reports.