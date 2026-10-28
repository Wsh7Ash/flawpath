# Usage

## Setup

```shell
python -m pip install -e ".[dev]"
flawpath validate      # must print: flawpath: 50/50 skills valid
python -m pytest -q    # 23 passed
```

Python 3.10+, no runtime dependencies.

## Day-to-day commands

| Command | What it does |
|---|---|
| `flawpath validate` | Runs every corpus rule **and** checks `skills/**/SKILL.md` on disk against a fresh render. Exit 0 only at 50/50. |
| `flawpath validate --skip-files` | Validates the authored corpus without touching generated files (useful mid-edit). |
| `flawpath validate --json` | Machine-readable report: checked, valid, passed, floors, issues. |
| `flawpath list` | All 50 skills with their phase. |
| `flawpath list --phase probe` | Narrow to one phase (19 skills). |
| `flawpath list --tag mass-assignment` | Narrow to one tag. |
| `flawpath show <slug>` | Print one rendered `SKILL.md`. |
| `flawpath search <terms...>` | Rank skills by keyword across slug, title, summary, tags and steps. |
| `flawpath build` | Regenerate `skills/`, `pack.json`, `results/catalog.md` and `results/validation.json`. |

## Turning a handler inventory into an assessment plan

```shell
flawpath flawplan --inventory-file examples/demo-inventory.json
flawpath flawplan --inventory-file examples/demo-inventory.json --top 6 --json
```

```text
# Assessment plan - orders service
Framework: express-style router with a body parser middleware   Routes: 3   Parameters: 5   Skills matched: 50 of 50   Plan steps: 12   Phases covered: 6/6

Routes: /api/v1/orders, /api/v1/orders/:id, /internal/reindex
Parameter sources: path, query, body, header, cookie

## scope
...
```

Inventory keys consumed as vocabulary: `routes`, `framework`, `parameters`, `auth_model`, `objects`, `observed`, `concerns`, `keywords`. Within nested objects, both key names and values are scored. Anything else in the file is ignored rather than guessed at.

- **`--top N`** caps plan length; selection is round-robin across phases, so every matched phase gets a slot before any phase gets a second.
- **Thin coverage** lists phases where the inventory matched *no* skill at all. It is computed from matches, never from the truncated plan.

## Loading skills into agents

Every skill is a standalone file with YAML front-matter:

```text
skills/unknown-field-acceptance/SKILL.md
```

**Claude Code** — point `skills` at this repository in `.claude/settings.json`, or copy the directory you want into the project's skills folder:

```json
{ "skills": { "paths": ["../flawpath/skills"] } }
```

**opencode** — add the directory to `opencode.json`:

```json
{ "skill": [{ "path": "../flawpath/skills" }] }
```

Any runtime that loads `SKILL.md` files works the same way; front-matter carries `name`, `description`, `pack`, `version`, `category` and `tags`.

## Regeneration discipline

`skills/**` and `pack.json` are **generated**. Never hand-edit them — a drift test will fail.

```shell
# 1. edit the corpus in src/flawpath/corpus/part1..3.py
# 2. regenerate and check the gate
flawpath build
flawpath validate      # must print 50/50
python -m pytest -q
```

CI runs the same sequence and then `git diff --exit-code -- skills pack.json results`, so a corpus edit committed without a rebuild fails the build.