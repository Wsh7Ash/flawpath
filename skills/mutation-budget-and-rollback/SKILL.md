---
name: mutation-budget-and-rollback
description: "Agree a numeric cap on write operations and a rollback step for each, so a probe that mutates state cannot quietly become the incident being investigated. Use when the plan includes write operations and no numeric cap or rollback sequence has been agreed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, rate-limit, operations]
---

# Mutation Budget and Rollback

> Agree a numeric cap on write operations and a rollback step for each, so a probe that mutates state cannot quietly become the incident being investigated

**Use when:** the plan includes write operations and no numeric cap or rollback sequence has been agreed

**Avoid when:** the boundary already states a mutation ceiling and provides a documented rollback

## Procedure

1. Record a numeric ceiling: mutations per endpoint and a total for the session, with a pause between probe families.
2. Write the rollback step for each class of mutation before performing any of them, not afterwards.
3. Set a stop condition tied to observed behaviour, such as a queue depth or an error rate, rather than to a planned step count.
4. Check whether the API applies rate limits itself, since hitting them changes what your results mean.
5. Log actual mutations beside the plan so the owner can see the session stayed inside the budget.
6. Perform the rollbacks at the end and record their results alongside the creations.

## Signals

- The plan mutates state with no stated ceiling anywhere
- A rollback step was never written and cannot be recalled under time pressure
- An error rate rose during the session without a stop condition to catch it
- The API's own rate limit began returning responses partway through

## Patterns

**1. Budget record**

```text
per_endpoint: 10 | session_total: 150 | pause: 5s | stop: any 5xx increase or queue depth > threshold | actual: 62
```

**2. Rollback first**

```text
write the rollback before the first mutation: rollback step, expected result, and what to do if it fails
```

**3. Rate-limit note**

```text
when the API's own limit returns 429, record it: it marks both your ceiling and a real behavioural observation
```

## Pitfalls

- Discovering the rollback procedure after a write did something unexpected
- Treating a 429 as a bug to report when it is the system working as designed
- Ending a session without the rollbacks having run

## Done when

- A numeric mutation ceiling and per-class rollback steps exist before the first write
- Actual mutations and rollback results are recorded beside the plan

## References

- [NIST SP 800-53 - Configuration and change controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - API rate limiting guidance](https://owasp.org/API-Security/)
