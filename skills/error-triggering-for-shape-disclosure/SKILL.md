---
name: error-triggering-for-shape-disclosure
description: "Trigger controlled errors and read what the shape discloses, because an error that names a field, a query or a stack is an exposure no input-side check will catch. Use when the error map exists and the leakage question has not been examined per shape"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, errors, disclosure]
---

# Error Triggering for Shape Disclosure

> Trigger controlled errors and read what the shape discloses, because an error that names a field, a query or a stack is an exposure no input-side check will catch

**Use when:** the error map exists and the leakage question has not been examined per shape

**Avoid when:** every error returns one uniform shape with only a correlation id

## Procedure

1. Choose controlled triggers: unknown identifier, malformed body, unsupported method and an authorization failure.
2. Send each at the agreed rate and capture status, body and timing against the error map baseline.
3. Compare shapes for disclosure: field names, query structure, internal identifiers, stack frames or versions.
4. Check whether the same condition yields different shapes in different environments, which the delta should explain.
5. Record which disclosures are externally visible as opposed to appearing only in server logs.
6. Record a leakage table with one row per trigger and the markers it exposes.

## Signals

- An error body names an internal field or a query fragment
- A stack trace or a version string appears in a response
- Two environments return different shapes for the same trigger
- Diagnostic detail intended for operators is returned to the caller

## Patterns

**1. Leakage table**

```text
trigger | status | marker | leaks | external
unknown id | 404 | {code} | nothing | yes
bad body | 400 | field names list | schema | yes
unhandled | 500 | stack frames | internals | yes
```

**2. Visibility column**

```text
external marks what a caller sees; a marker only in server logs is an operator concern, not a disclosure finding
```

**3. Baseline comparison**

```text
each shape is compared against the map captured earlier, so a difference is recognisable as a difference
```

## Pitfalls

- Reporting operator log detail as an external leak without checking where it appeared
- Comparing shapes across environments and blaming the application for a debug setting
- Triggering errors that create load rather than choosing controlled, bounded ones

## Done when

- Each controlled trigger has a recorded status, marker and visibility
- Disclosures are split into externally visible and server-log-only

## References

- [CWE-209 - Generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)
- [OWASP - Error handling guidance](https://owasp.org/www-project-web-security-testing-guide/)
