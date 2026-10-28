# Contributing

Thanks for helping improve `flawpath`.

## Ground rules

- **Authorized-use scope only.** Contributions must stay defensive or methodology-focused: no exploit payloads, no instructions for accessing systems the reader does not own or have written permission to test.
- **No live data.** Never commit real credentials, customer records, internal hostnames or private address literals. Synthetic fixtures only.
- **One skill, one job.** A skill must be a single self-contained procedure with a clear "use when" and "avoid when".
- **No network calls.** The package stays stdlib-only and offline at runtime.
- **Keep the ordering.** `scope` and `map` must precede `probe` in `PHASE_ORDER`; a test asserts it.

## Adding or editing a skill

1. Edit the corpus in `src/flawpath/corpus/part1.py`–`part3.py` (the source of truth). Do **not** hand-edit `skills/**/SKILL.md`; generated files are overwritten and a drift test will fail.
2. Regenerate and check the gate:

   ```shell
   flawpath build
   flawpath validate   # must print 50/50
   python -m pytest -q
   ```

3. Keep counts honest: adding a skill requires removing or merging another to keep the corpus at 50, or raising `expected_skills` deliberately in `corpus/__init__.py` together with a note in the PR.
4. If you add a phase, extend `PHASE_ORDER` in `corpus/__init__.py`, update the phase assertions in `tests/test_corpus.py`, and keep `scope` first.

## Quality floor enforced by CI

| Rule | Floor |
|---|---|
| Steps / signals / patterns / pitfalls / done-when | 6 / 4 / 3 / 3 / 2 |
| Rendered words per skill | >= 180 |
| Pattern label / code | >= 8 / >= 20 chars, no code fences |
| References | canonical `[label](https://...)`, >= 1 |
| Slugs and titles | unique, lowercase kebab-case |
| Summary / use-when / avoid-when | >= 40 / 30 / 30 chars |
| Description (front-matter) | 120-1024 chars |
| Hygiene | no placeholder tokens, no machine-local paths, no live credentials, no private addresses |

## Pull requests

- Keep one concern per PR (one skill family, one rule change, one CLI feature).
- Include the output of `validate` and `pytest` in the description.
- Update `CHANGELOG.md` and `RESULTS.md` when behaviour changes.