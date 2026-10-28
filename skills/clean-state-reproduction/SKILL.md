---
name: clean-state-reproduction
description: "Reproduce an observation from a fresh record and an empty cache, so a reviewer can replay it without inheriting the state your earlier probes created. Use when an observation must be handed to an owner or reviewer who will replay it elsewhere"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [confirm, reproduction, method]
---

# Clean-State Reproduction

> Reproduce an observation from a fresh record and an empty cache, so a reviewer can replay it without inheriting the state your earlier probes created

**Use when:** an observation must be handed to an owner or reviewer who will replay it elsewhere

**Avoid when:** the behaviour is deterministic and cannot depend on prior state, which a repeat already proved

## Procedure

1. Identify every store that could remember your earlier requests: record state, caches, rate limiters and idempotency keys.
2. State which must be empty before step one and how a reader clears or avoids each.
3. Use a fresh synthetic record and a fresh key for each run so no run inherits another's state.
4. Write the request sequence in order, including waits, so it can be replayed without interpretation.
5. Record the status and the observable outcome for each step so a reader can tell a match from a divergence.
6. Package the recipe with the observation and mark any step that cannot be replayed outside your session.

## Signals

- The reproduction succeeds on your machine but fails for a reviewer with a warm cache
- The first request of a session behaves differently from every later one
- A step has no recorded outcome, leaving the state at that point ambiguous
- The recipe depends on a record or key created by an earlier probe

## Patterns

**1. Recipe block**

```text
precondition: cache empty, fresh record R1
1. POST create key K1 -> record status
2. PATCH unknown field -> record status
3. GET R1 -> record full field set
record every outcome
```

**2. Fresh-key rule**

```text
each run uses a new record and a new idempotency key, suffixed with the run number, so no run inherits another's state
```

**3. Assumption list**

```text
if a step cannot be replayed outside your session, write it as an environment assumption rather than presenting it as deterministic
```

## Pitfalls

- Writing a reproduction that silently relies on state your earlier probe created
- Omitting the empty-store precondition, so a reviewer sees a different result and reports a false negative
- Presenting an environment-dependent sequence as though it were deterministic

## Done when

- A numbered recipe lists every request with its outcome and the stores that must be empty first
- The recipe reproduces in a fresh context without relying on state from earlier runs

## References

- [PortSwigger - Writing reproducible reports](https://portswigger.net/web-security)
- [NIST - Evidence handling guidance](https://csrc.nist.gov/publications/detail/sp/800-86/final)
