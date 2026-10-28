# Security Policy

## Authorized use only

`flawpath` is a knowledge corpus and planning tool for **authorized** security work: assessing APIs you own, or programs whose rules explicitly permit the testing you perform. The software itself performs **no network requests** — it renders, validates and plans locally from a JSON inventory you supply.

The skills describe backend **assessment** methodology: how to map what a handler accepts, which probes are in scope, how to attribute an outcome to a single input, how to fix it in framework terms and how to report it. They contain no weaponized exploit material.

## What this corpus deliberately does not contain

- No exploit payloads, proof-of-concept attack code or automation against third parties.
- No instructions for attacking a system without written authorization.
- No credential harvesting, session theft, phishing or evasion guidance.
- No live target data, credentials or personal data. The example inventory uses `/api/v1/orders` paths and synthetic object names only.

## Scope discipline is built into the corpus

The opening skills exist to keep an assessment bounded and honest:

1. `api-assessment-boundary` — paths, methods, write permissions and the rate ceiling are written down before the first request of every session.
2. `synthetic-record-only-policy` — every write targets a marked record you created, checked four ways before it is sent.
3. `mutation-budget-and-rollback` — a numeric ceiling and a rollback step exist *before* the first mutation, not after one goes wrong.
4. `single-input-attribution` — a probe that changed three inputs supports no causal claim, and the confirm phase exists to catch exactly that.

`flawplan` always emits `scope` first, and a test asserts `scope` and `map` precede `probe` in `PHASE_ORDER`: a plan that starts probing before it has a boundary and a parameter map has skipped the two steps that make a later finding defensible.

## Reporting a vulnerability in this project

If you find a defect in `flawpath` itself — for example, a validation bypass that lets a malformed skill pass the 50/50 gate — please open a private security advisory on the repository or contact the maintainer through GitHub. Do not publish exploit details before a fix is available.

## Scope of this project's own testing

All tests run locally against the checked-in corpus and the checked-in example inventory. No test sends traffic anywhere; `flawplan` reads one JSON file and scores text. Continuous integration runs the same local gates: validation, unit tests and an artifact-sync check.