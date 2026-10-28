---
name: partial-update-omission-behavior
description: "Establish what an omitted field does during a partial update, because an omission that resets to default is a mutation the caller never asked for. Use when the API supports partial updates and the semantics of omitted fields are unconfirmed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, patch, state]
---

# Partial Update Omission Behavior

> Establish what an omitted field does during a partial update, because an omission that resets to default is a mutation the caller never asked for

**Use when:** the API supports partial updates and the semantics of omitted fields are unconfirmed

**Avoid when:** omitted fields are documented as unchanged and a test confirms the stored value survives

## Procedure

1. Capture the full state of a synthetic record you own before the update.
2. Send a partial update touching one field while omitting several others.
3. Read the record back and compare every field against the captured state, not only the one you sent.
4. Identify any omitted field that changed, reset or lost precision as a side effect.
5. Repeat once with a different subset omitted to confirm the behaviour is about omission rather than the field.
6. Record which fields are preserved, reset or recomputed on omission.

## Signals

- An omitted field resets to a default rather than keeping its value
- A numeric or precision-bearing field changes when it was not mentioned
- A nested object is replaced wholesale when only a sibling field was updated
- The behaviour differs between two subsets of omitted fields

## Patterns

**1. Diff record**

```text
before: {a: 1, b: 2, c: 3}
update: {b: 9}
after:  {a: 1, b: 9, c: 0}  <- omitted c reset
```

**2. Full-diff rule**

```text
compare every field rather than only the one you sent; the side effect is on a field you did not touch
```

**3. Subset repeat**

```text
a second omission subset separates a field-specific behaviour from a general omission rule
```

## Pitfalls

- Checking only the field that was sent, which is exactly how a reset goes unnoticed
- Attributing a reset to the update when it was caused by a server-side recompute
- Concluding safe behaviour from one subset and never varying it

## Done when

- Every field on the record is diffed before and after the partial update
- Preserved, reset and recomputed fields are listed with a confirming second subset

## References

- [RFC 5789 - PATCH method for HTTP](https://www.rfc-editor.org/rfc/rfc5789)
- [CWE-642 - External control of critical state data](https://cwe.mitre.org/data/definitions/642.html)
