# Project Spec — flawpath

## Name

`flawpath`

## Category

`backend-api`

## Target user

Engineers and authorized testers reviewing server-side implementation of an API: handlers, middleware, request schemas and the state they touch.

## Problem

Backend implementation defects are found by reading, and the reading is never recorded. Which fields the parser passes through; whether validation runs before or after object construction; what an omitted field does during a partial update; whether two content types reach two parsers with different policies; which error shape came from which layer; whether the middleware chain in configuration matches the one in documentation. Every assessment re-derives that map from scratch, and when a probe turns up something real nobody else can replay it because the map lived in one person's head. Agents have no structured skill files to load either, so the same five questions get asked in every engagement.

## Solution

A corpus of 50 unique, validated backend implementation skills organised into six phases (`scope`, `map`, `probe`, `confirm`, `harden`, `document`), a validator that enforces quality floors, and a `flawplan` CLI that turns a handler inventory into a phase-ordered assessment plan with honest thin-coverage reporting.

## Core workflow

```text
author/edit corpus  ->  build  ->  skills/ + pack.json + results/
                                    |
                                    v
                          validate (50/50 gate)  ->  pytest  ->  CI
                                    |
                                    v
                       flawplan --inventory-file inventory.json -> ordered plan
```

## Must-have features

- 50 unique skills with unique slugs and titles across the six phases.
- Validator with structural, strength and hygiene rules; exit `0` only at 50/50.
- Deterministic renderer; committed files proven in sync by tests.
- `flawplan` producing a phase-ordered plan from a JSON inventory, with thin coverage derived from matches rather than from the truncated plan.
- `scope` and `map` must precede `probe` in `PHASE_ORDER`, asserted by a test.

## Nice-to-have (explicitly out of scope for v1)

- A fuzzer or traffic generator. The pack makes **no** network requests.
- Automatic route discovery from source.
- A scoring model beyond the precondition/effect/boundary statement the corpus describes.

## Acceptance tests

1. `validate` exits 0 and reports 50/50.
2. `pytest -q` passes 23 tests, including regeneration equality, drift detection, the scope-before-probe ordering and the absence of live credentials.
3. `flawplan` — round-trips the checked-in example inventory, covers all 6 phases with `--top 6`, and reports every phase as thin coverage for an inventory that matches nothing.
4. A generated build lands byte-identically in a clean temp directory.

## Authorized-use constraint

This is a defensive and methodology pack. Skills describe mapping and probes performed under a written boundary against synthetic records you own, confirmation from local evidence, framework-level fixes and reporting. The corpus contains no weaponized payload, no exploit chain and no live target data; `SECURITY.md` states the boundary and the reporting path.