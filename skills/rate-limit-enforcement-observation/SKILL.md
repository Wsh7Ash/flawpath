---
name: rate-limit-enforcement-observation
description: "Observe which requests the rate limiter counts and which it lets through, because a limit enforced on the wrong key protects nothing while still appearing configured. Use when a rate limiter is documented or configured but its enforcement key has not been observed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, rate-limit, resources]
---

# Rate Limit Enforcement Observation

> Observe which requests the rate limiter counts and which it lets through, because a limit enforced on the wrong key protects nothing while still appearing configured

**Use when:** a rate limiter is documented or configured but its enforcement key has not been observed

**Avoid when:** the limiter's key and behaviour are documented and a test confirms them

## Procedure

1. Record the documented limit, its window and the key it is said to use, before sending anything.
2. Send requests within your own budget until a limit or a header appears, staying under the boundary ceiling.
3. Read the limit headers to learn remaining, reset and the key the server appears to count by.
4. Vary one dimension between requests to see whether the counter follows identity, ip, or neither.
5. Record whether an unauthenticated request shares a counter with an authenticated one.
6. State the enforcement key you observed alongside the documented one, and any difference.

## Signals

- The enforced key differs from the documented one
- Authenticated and unauthenticated requests share one counter
- The limiter counts only successful responses, so failed requests are unbounded
- No limit headers appear at all, leaving enforcement unobservable

## Patterns

**1. Enforcement record**

```text
documented: per api key, 100/min | observed: headers show counter shared across identities | verdict: enforced by ip, not by key
```

**2. Header read**

```text
remaining, reset and limit headers recorded per response; their absence is recorded too, since it means enforcement is unobservable
```

**3. Boundary check**

```text
the test stays inside your own rate budget, because proving a limit by exceeding it breaches the ceiling you agreed
```

## Pitfalls

- Exceeding your own rate budget to prove that a limit exists
- Assuming the documented key is the enforced one without varying a dimension
- Reporting a missing limiter when it is simply not observable from headers

## Done when

- The documented and observed enforcement keys are both recorded with the evidence
- Limit headers, or their absence, are captured for each request class tested

## References

- [OWASP - API rate limiting guidance](https://owasp.org/API-Security/)
- [CWE-770 - Allocation of resources without limits](https://cwe.mitre.org/data/definitions/770.html)
