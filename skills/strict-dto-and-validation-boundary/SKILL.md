---
name: strict-dto-and-validation-boundary
description: "Give every write path a strict request object that rejects unknown, mistyped and out-of-range input before construction, so the handler only ever sees declared shape. Use when validation is loose, applied after construction, or varies by content type"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [harden, validation, schema]
---

# Strict DTO and Validation Boundary

> Give every write path a strict request object that rejects unknown, mistyped and out-of-range input before construction, so the handler only ever sees declared shape

**Use when:** validation is loose, applied after construction, or varies by content type

**Avoid when:** a strict request object already governs every write path and a test confirms rejection

## Procedure

1. Define a request object per endpoint with declared fields, types, ranges and enumerations.
2. Configure it to reject unknown fields rather than discard them, so a client error is visible instead of silent.
3. Run it before object construction, so nothing unvalidated is ever built.
4. Apply the same object regardless of which parser produced the request, since parser choice must not change policy.
5. Return one uniform rejection for all validation failures with a correlation id.
6. Re-run the coercion, range, duplicate-key and content-type probes against the change.

## Signals

- Validation runs after an object is constructed from the parsed body
- Unknown fields are silently discarded rather than rejected
- Different parsers yield different validation behaviour for the same bytes
- Validation failures return several distinct error shapes

## Patterns

**1. Target order**

```text
parse -> validate (strict, reject unknown) -> construct -> handle; the validator runs before anything is built
```

**2. Reject-not-strip**

```text
rejection tells the caller their request was wrong; silent stripping hides a client bug and makes support harder
```

**3. Retest set**

```text
re-run coercion, range, duplicate-key and content-type probes; each must now produce the same uniform rejection
```

## Pitfalls

- Adding validation after construction, which still allows transient invalid state
- Stripping unknown fields quietly, which fixes the exposure while hiding the client error
- Validating only the default parser path while a second content type reaches the handler unvalidated

## Done when

- Each write path has a strict request object that rejects unknown input before construction
- The four original probes are re-run with results recorded

## References

- [OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [CWE-20 - Improper input validation](https://cwe.mitre.org/data/definitions/20.html)
