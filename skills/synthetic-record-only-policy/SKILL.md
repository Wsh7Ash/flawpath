---
name: synthetic-record-only-policy
description: "Create and mutate only records you own, so a write-surface assessment never leaves real customer data changed or a real workflow triggered. Use when the assessment will create or update records through the API"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, data-handling, safety]
---

# Synthetic Record Only Policy

> Create and mutate only records you own, so a write-surface assessment never leaves real customer data changed or a real workflow triggered

**Use when:** the assessment will create or update records through the API

**Avoid when:** the environment runs entirely on fixtures that no real record can reach

## Procedure

1. Create a synthetic record set under an account you control, with invented identifiers and values.
2. Mark those records with a recognizable marker so a later cleanup can find them without a query you have to trust.
3. Check every write you plan against the boundary: permitted method, permitted path, rollback available.
4. Avoid any write that triggers an external effect, such as a notification or a charge, unless the boundary explicitly permits it.
5. Record the identifiers of every record you created so cleanup is mechanical rather than archaeological.
6. Clean up at the end and record what was removed and what could not be.

## Signals

- A test write would trigger a notification or a charge to someone
- No marker distinguishes records you created from records that already existed
- Created records are never cleaned up, so they accumulate in the environment
- A write targets an existing record rather than one you created

## Patterns

**1. Synthetic marker**

```text
owner: tester@example.test | note: authorized assessment fixture | created: 2026-10-28 | cleanup: scheduled
```

**2. Write check**

```text
before each write: method permitted? path permitted? rollback exists? external effect avoided? all four yes before sending
```

**3. Cleanup list**

```text
identifiers created, removed at <time>, exceptions recorded; stored beside the boundary so the session leaves nothing behind
```

## Pitfalls

- Updating a record you did not create because it was convenient to test against
- Triggering a real notification to prove a field reaches a template
- Leaving fixture records behind because cleanup was planned but never scheduled

## Done when

- Every write targets a marked record you created, with the four-part write check recorded
- A cleanup list exists with what was removed and any exceptions

## References

- [OWASP - Sensitive data exposure](https://owasp.org/www-project-top-ten/)
- [NIST SP 800-53 - Information handling controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
