---
name: reproduction-steps-in-client-terms
description: "Write the reproduction so someone else can run it with their own client and fixtures, using plain requests rather than the tooling only you had set up. Use when an owner must independently reproduce a finding before acting on it"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [document, reproduction, handover]
---

# Reproduction Steps in Client Terms

> Write the reproduction so someone else can run it with their own client and fixtures, using plain requests rather than the tooling only you had set up

**Use when:** an owner must independently reproduce a finding before acting on it

**Avoid when:** the owner has already reproduced the observation themselves

## Procedure

1. Rewrite the sequence as plain requests: method, path, headers and body, with placeholders for the reader's own identifiers.
2. State the preconditions: an account, a role, a record to create, and the environment.
3. Give expected output per step, so the reader can tell a match from a divergence.
4. List the environmental assumptions, such as a feature flag or a configuration value, that the result depends on.
5. Run the published version yourself from a clean state and confirm the expected output still appears.
6. Mark which findings depend on this recipe for reproduction and which reproduce from the evidence alone.

## Signals

- The owner replies that the observation does not reproduce on their side
- The recipe contains steps that only work with state your session created
- Expected output is described in prose rather than as values to match
- Environmental assumptions such as a flag or a mode are unstated

## Patterns

**1. Published recipe**

```text
precondition: account with member role, empty cache
1. POST /orders (key K1) -> expect 201, id R1
2. PATCH /orders/R1 {status, undeclared: true} -> expect 200
3. GET /orders/R1 -> expect undeclared absent
```

**2. Assumption list**

```text
assumes: strict validation off in this environment, no feature flag routing elsewhere; listed so a divergence has an explanation
```

**3. Dependency note**

```text
findings F-01 and F-03 require this recipe; F-02 reproduces from the evidence block alone
```

## Pitfalls

- Publishing a recipe that depends on an idempotency key or record from an earlier probe
- Omitting an environment flag, then reading a configuration difference as a failed reproduction
- Never re-running the published version, so a later change invalidates it unnoticed

## Done when

- The published recipe runs from a clean state and produces the stated expected output
- Environmental assumptions and dependent findings are listed beside it

## References

- [PortSwigger - Writing reproducible reports](https://portswigger.net/web-security)
- [OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)
