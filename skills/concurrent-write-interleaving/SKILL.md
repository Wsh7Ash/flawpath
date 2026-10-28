---
name: concurrent-write-interleaving
description: "Issue two writes to the same record together and read the result, because an unguarded update lets the later write silently discard the earlier one. Use when the API permits concurrent updates to one record and the interleaving behaviour is unconfirmed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, concurrency, state]
---

# Concurrent Write Interleaving

> Issue two writes to the same record together and read the result, because an unguarded update lets the later write silently discard the earlier one

**Use when:** the API permits concurrent updates to one record and the interleaving behaviour is unconfirmed

**Avoid when:** an optimistic locking or version field is enforced and a test confirms a conflict is rejected

## Procedure

1. Confirm the boundary permits concurrent requests and that a rollback exists for the record.
2. Capture the record's state, then send two updates touching different fields at the same time.
3. Read the record back and record whether both changes survived or one was lost.
4. Repeat if the first attempt happened to serialize by timing, since a clean result may just be luck.
5. Check for a version, etag or updated-at guard in the request and response.
6. Record the observed behaviour as guarded, lost update, or serialized by timing with evidence.

## Signals

- Two updates to different fields result in only one surviving
- No version or etag guard appears in the request or response contract
- The record's updated-at is identical after two logically separate writes
- A repeat of the test yields a different outcome, indicating timing dependence

## Patterns

**1. Interleaving record**

```text
write A {field1} and write B {field2} sent together -> read-back: field1 unchanged, field2 applied; verdict: lost update
```

**2. Guard check**

```text
look for version, etag or updated-at in both directions; absence is recorded as no guard rather than as safe by default
```

**3. Repeat rule**

```text
a single clean run may be serialization by luck; repeat enough times to state the behaviour honestly
```

## Pitfalls

- Concluding safe behaviour from one run that happened to serialize
- Changing two fields in one request rather than issuing two requests
- Reporting a lost update without noting whether a guard field exists but was not supplied

## Done when

- Two concurrent writes have a recorded read-back showing which changes survived
- The presence or absence of a version guard is stated, with repeats to rule out luck

## References

- [CWE-362 - Concurrent execution using shared resource with improper synchronization](https://cwe.mitre.org/data/definitions/362.html)
- [OWASP - Race condition guidance](https://owasp.org/www-project-web-security-testing-guide/)
