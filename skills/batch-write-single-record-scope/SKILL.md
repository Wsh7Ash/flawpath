---
name: batch-write-single-record-scope
description: "Send a batch containing many entries and one that differs from the rest, because a batch that mutates as a unit can change records you never intended to touch. Use when the API accepts an array or batch of items for a write operation"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, batch, writes]
---

# Batch Write Single-Record Scope

> Send a batch containing many entries and one that differs from the rest, because a batch that mutates as a unit can change records you never intended to touch

**Use when:** the API accepts an array or batch of items for a write operation

**Avoid when:** each batch item is processed independently and a test confirms partial failure isolates correctly

## Procedure

1. Confirm the boundary permits batch writes and identify the rollback for the whole batch.
2. Send a small batch where one item is intentionally different from the others on records you own.
3. Read back every record in the batch and record which items were applied and which were not.
4. Check whether the response reports per-item results or only an overall status.
5. Determine whether the batch is atomic: all applied, or none applied, or a partial state.
6. Record the batch's atomicity, reporting granularity and any item that behaved differently.

## Signals

- A partial failure applies some items and reports only an overall success
- One item in the batch is processed differently from the rest with no per-item status
- The batch is neither atomic nor reported per item, leaving a partial state invisible
- An item's result cannot be determined from the response at all

## Patterns

**1. Batch record**

```text
items: 3 (2 same, 1 different) | response: overall 200 | read-back: 3 applied | per-item status: absent | atomicity: none observed
```

**2. Partial-state rule**

```text
the interesting outcome is a partial application with an overall success response; that pairing is what the report states
```

**3. Reporting gap**

```text
no per-item status means a caller cannot tell which items failed, recorded as its own finding
```

## Pitfalls

- Reporting an overall status as proof every item succeeded without reading each record back
- Making a batch too large to attribute an effect to a single item
- Overlooking that a partial state may persist because nothing rolls it back

## Done when

- Every item in the test batch has a read-back result recorded
- Atomicity and per-item reporting are each stated explicitly

## References

- [OWASP - API security guidance](https://owasp.org/API-Security/)
- [CWE-841 - Improper enforcement of behavioral workflow](https://cwe.mitre.org/data/definitions/841.html)
