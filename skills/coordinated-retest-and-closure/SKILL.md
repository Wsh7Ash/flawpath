---
name: coordinated-retest-and-closure
description: "Agree the retest point in writing, re-run the original probe after the fix lands, and close only on the observed result rather than on the promise that it was done. Use when a finding has been fixed and is about to be reported as closed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [document, verification, closure]
---

# Coordinated Retest and Closure

> Agree the retest point in writing, re-run the original probe after the fix lands, and close only on the observed result rather than on the promise that it was done

**Use when:** a finding has been fixed and is about to be reported as closed

**Avoid when:** the fix is still in progress and closure is not yet being considered

## Procedure

1. Agree the retest point, the target date and the person who will run it, in writing, before the fix lands.
2. Re-run the exact probe from the evidence pack against the same class of record in the same environment.
3. Record the new status, body and read-back result beside the original evidence entry.
4. Re-run the regression check if one exists, since a check that passes independently is stronger evidence.
5. Close only when the observed result matches the expectation, and record the date and the person who confirmed it.
6. List anything still open with its blocker and owner, since an unfixable finding needs a decision rather than a status.

## Signals

- Closure was announced without the original probe being re-run
- The retest used a different request than the one that found the defect
- A regression check exists but was not run during closure
- Items remain open with no owner and no date attached

## Patterns

**1. Closure record**

```text
F-01 | retest 2026-10-28 by <owner> | probe replayed: field absent on read-back | regression check: pass | closed
```

**2. Same-request rule**

```text
re-run the identical request that found the defect; a different request answers a different question
```

**3. Open-items list**

```text
open item | blocker | owner | needed decision; listed so it is escalated rather than left in a backlog
```

## Pitfalls

- Closing on a merge request hash instead of on the observed result
- Retesting with a different request than the original and calling the difference a pass
- Leaving a blocked finding in the list without naming who can unblock it

## Done when

- Each closed finding has a retest record with date, observer and the replayed probe result
- Open items name their blocker and the person who can unblock them

## References

- [NIST SP 800-53 - Assessment and monitoring records](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)
