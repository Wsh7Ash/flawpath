---
name: server-side-field-allowlist
description: "Build the accepted field set on the server from an explicit allow-list, so a field nobody declared can never reach an assignment no matter how the parser behaves. Use when the parser passes unknown keys through or a probe showed an undeclared field was stored"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [harden, mass-assignment, validation]
---

# Server-Side Field Allowlist

> Build the accepted field set on the server from an explicit allow-list, so a field nobody declared can never reach an assignment no matter how the parser behaves

**Use when:** the parser passes unknown keys through or a probe showed an undeclared field was stored

**Avoid when:** an explicit allow-list already governs assignment and a probe confirms rejection

## Procedure

1. Declare the accepted field set per endpoint explicitly, in code or schema, rather than deriving it from a model.
2. Apply the allow-list at the assignment boundary, after parsing and before any write to state.
3. Reject or strip anything not on the list, and record which of the two you chose and why.
4. Include nested paths in the declaration so a dotted or bracketed key cannot reach an undeclared field.
5. Re-run the unknown-field, privileged-field and nested-key probes against the change.
6. Record the change location and the retest results beside it.

## Signals

- The accepted set is derived from the model, which by construction includes every persisted field
- Stripping is applied only in some code paths while others assign directly
- Nested paths are not declared, so a dotted key bypasses the flat allow-list
- The retest after the change was never run

## Patterns

**1. Declaration**

```text
endpoint: PATCH /orders/{id} -> allowed: [status, note, shipping_address.street, shipping_address.city]
```

**2. Placement**

```text
parse -> allow-list -> assign -> persist; an allow-list applied before parsing is bypassed by whatever the parser produces
```

**3. Retest set**

```text
re-run unknown-field, privileged-field and nested-key probes; all three must now be rejected with the same response
```

## Pitfalls

- Deriving the allow-list from the model, which is the defect restated as a fix
- Declaring only flat fields while nested paths remain writable
- Declaring the change without re-running the probes that found the problem

## Done when

- An explicit field declaration exists per endpoint and is applied at the assignment boundary
- The three original probes are re-run and their results recorded

## References

- [OWASP - Mass assignment guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)
