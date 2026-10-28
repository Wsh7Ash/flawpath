# Changelog

All notable changes to `flawpath` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [1.0.0] - 2026-10-28

### Added

- Initial release: 50 unique backend implementation skills across six phases
  (`scope`, `map`, `probe`, `confirm`, `harden`, `document`).
- Validator with structural, strength and hygiene rules; `50/50 skills valid`
  gate with `--json` output for CI.
- Deterministic renderer and `build` command writing `skills/`,
  `pack.json` (SHA-256 per skill) and `results/`.
- CLI: `validate`, `list`, `show`, `search`, `build`, `flawplan`.
- `flawplan` — handler inventory to phase-ordered assessment plan, with
  phase-stratified selection and match-derived thin-coverage reporting.
- Example inventory `examples/demo-inventory.json`.
- Test suite (23 tests) covering corpus shape, rules, regeneration, drift,
  scope-before-probe ordering, credential hygiene, every CLI command and
  flawplan's selection semantics.
- CI workflow, docs (`ARCHITECTURE`, `USAGE`, `PROJECT_SPEC`), `SECURITY.md`.

### Design notes

- `missing_phases` is derived from matched skills, not from the plan truncated
  by `--top`, so a covered phase can never be reported as uncovered.
- Selection draws matches round-robin across `PHASE_ORDER` before any phase
  receives a second slot, so `--top 6` still covers all six phases when the
  inventory matches them.
- Vocabulary flattening scores dict **keys** as well as values, so a setting
  named `unknown_field_policy` describes the receiver as much as its value.
- `test_scope_phase_always_precedes_probes` asserts that `scope` and `map`
  precede `probe`, so the pack's own ordering discipline cannot drift.