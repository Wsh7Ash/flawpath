---
name: deserialization-and-validation-boundary
description: "Locate exactly where a request body becomes application objects and where validation runs relative to it, because everything downstream of an unvalidated parse inherits the risk. Use when the request body is parsed into objects and the ordering of parse, validate and authorize is unconfirmed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, parsing, validation]
---

# Deserialization and Validation Boundary

> Locate exactly where a request body becomes application objects and where validation runs relative to it, because everything downstream of an unvalidated parse inherits the risk

**Use when:** the request body is parsed into objects and the ordering of parse, validate and authorize is unconfirmed

**Avoid when:** a framework pipeline documents the order and the handler code confirms it

## Procedure

1. Find the point in the pipeline where the body is decoded and note what runs before and after it.
2. Determine whether validation runs before object construction or after, since the two orders differ in what they permit.
3. Check whether unknown fields are rejected, stripped or passed through by default.
4. Note which parser is used and whether more than one can parse the same request depending on content type.
5. Record whether authorization runs before or after the parse, since an unauthenticated parse is a resource question too.
6. Write the order as an explicit sequence so a later reader does not have to infer it.

## Signals

- Validation runs after object construction from the parsed body
- Unknown fields are passed through rather than rejected
- Two parsers can handle the same request depending on the content type header
- Authorization happens after the body has already been parsed

## Patterns

**1. Order record**

```text
receive -> parse body -> construct object -> validate -> authorize -> handle
any other order is recorded explicitly rather than assumed
```

**2. Unknown-field policy**

```text
reject | strip | pass through; record which applies by default, since pass-through is what mass assignment needs
```

**3. Parser list**

```text
content type -> parser used; a second parser for the same request is listed because it may apply a different policy
```

## Pitfalls

- Assuming validation precedes construction because that is how the framework is usually described
- Recording the documented order instead of reading the code path that runs
- Ignoring a second parser selected by content type

## Done when

- The parse, validate and authorize order is written as an explicit sequence with a code location
- The unknown-field policy and the parsers in play are recorded

## References

- [OWASP - Deserialization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [CWE-502 - Deserialization of untrusted data](https://cwe.mitre.org/data/definitions/502.html)
