---
name: regression-probe-suite
description: "Turn every probe that found something into a repeatable check that runs on every change, so the fix is protected rather than merely applied. Use when findings have been fixed and nothing currently prevents them returning"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [harden, regression, pipeline]
---

# Regression Probe Suite

> Turn every probe that found something into a repeatable check that runs on every change, so the fix is protected rather than merely applied

**Use when:** findings have been fixed and nothing currently prevents them returning

**Avoid when:** a suite already covers each finding and runs in the pipeline with fixture proof

## Procedure

1. For each finding, write the probe as a check with an explicit expected rejection or expected state.
2. Run the checks against the fix to prove they fail before it and pass after, which is what makes them meaningful.
3. Place them in the pipeline that runs on every change rather than in a scheduled job nobody reads.
4. Make the assertion about the specific behaviour, not only a status code, so a coincidental 400 does not pass.
5. Record which findings have a check and which do not, since the unchecked list is the remaining risk.
6. Assign an owner to the suite, because an unowned check stops being maintained within a quarter.

## Signals

- A check asserts only a status code, so any rejection passes it
- The check was never observed failing before the fix was applied
- Some findings have no check and the report does not say which
- No owner is assigned to maintaining the suite

## Patterns

**1. Check record**

```text
finding F-01 | probe: send unknown field | assert: field absent on read-back, not merely status 400 | owner: team-api
```

**2. Fail-then-pass**

```text
run the check against the pre-fix build and the post-fix build; both results recorded, since a check that never failed proves nothing
```

**3. Coverage list**

```text
findings with checks and without checks are both listed; the without list is what remains unprotected
```

## Pitfalls

- Asserting only a status code, so a different rejection satisfies the check
- Never observing the check fail, which means its strength is unknown
- Leaving the suite unowned so it decays as the code around it changes

## Done when

- Every finding has a named check with a behavioural assertion and an owner
- Each check is recorded as failing before the fix and passing after it

## References

- [OWASP - Security regression testing](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST SP 800-53 - Configuration change control](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
