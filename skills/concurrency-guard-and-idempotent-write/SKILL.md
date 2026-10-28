---
name: concurrency-guard-and-idempotent-write
description: "Add a version guard so concurrent updates conflict visibly, and enforce the idempotency key so a retried create cannot produce a second object. Use when a lost update or a duplicate create was observed during probing"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [harden, concurrency, idempotency]
---

# Concurrency Guard and Idempotent Write

> Add a version guard so concurrent updates conflict visibly, and enforce the idempotency key so a retried create cannot produce a second object

**Use when:** a lost update or a duplicate create was observed during probing

**Avoid when:** a version guard and an enforced idempotency key already exist and probes confirm both

## Procedure

1. Add a version or updated-at field to each mutable object and require it on every update.
2. Return a conflict status when the supplied version does not match, rather than silently last-write-wins.
3. Enforce the idempotency key by storing it with its first response and returning that response on replay.
4. Key the stored response on the request identity so a changed body with a reused key is rejected.
5. Re-run the interleaving and idempotency probes against the change and record the outcomes.
6. State what happens to concurrent requests that arrive together, since a guard moves the failure rather than removing it.

## Signals

- Two concurrent updates result in one silently overwriting the other
- A replayed create key produces a second object
- A reused key with a changed body is processed instead of rejected
- A conflict is returned as a generic error with no indication of the version mismatch

## Patterns

**1. Guard record**

```text
field: version | required on: update | mismatch: 409 with correlation id | last-write-wins: disabled
```

**2. Idempotency record**

```text
key storage: keyed to request identity, retained for <window> | replay: original response returned | changed body with same key: 409 rejected
```

**3. Retest expectation**

```text
re-run concurrent-write-interleaving and idempotency-key-handling; both must now show the guard working rather than the effect repeating
```

## Pitfalls

- Adding a version field but leaving the handler to overwrite on mismatch anyway
- Storing the idempotency key without binding it to the body, so a changed request returns a stale response
- Treating a conflict response as a fix without re-running the concurrent probe

## Done when

- Updates require a version and return a conflict on mismatch, with a recorded retest
- Idempotency keys are enforced and bound to request identity, with the replay retest recorded

## References

- [CWE-362 - Concurrent execution with improper synchronization](https://cwe.mitre.org/data/definitions/362.html)
- [CWE-841 - Improper enforcement of behavioral workflow](https://cwe.mitre.org/data/definitions/841.html)
