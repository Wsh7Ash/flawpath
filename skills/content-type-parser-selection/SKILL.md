---
name: content-type-parser-selection
description: "Vary the declared content type with identical bytes, because the parser the header selects decides which validation and which unknown-field policy your request actually gets. Use when the endpoint accepts more than one content type or falls back when the header is absent"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, content-type, parsing]
---

# Content-Type Parser Selection

> Vary the declared content type with identical bytes, because the parser the header selects decides which validation and which unknown-field policy your request actually gets

**Use when:** the endpoint accepts more than one content type or falls back when the header is absent

**Avoid when:** one content type is accepted and others are rejected before parsing

## Procedure

1. Send the same logical body under each accepted content type and with the header omitted entirely.
2. Capture status, body and which handler or parser the response suggests ran.
3. Include the unknown-field probe under each parser, since policies may differ between them.
4. Note whether an unexpected type routes to a different handler with its own validation step.
5. Rank each case by whether a real client can produce it, since that decides practical relevance.
6. Record a table of declared type, status, parser and validation outcome.

## Signals

- Omitting the content type falls back to a parser with weaker validation
- Two parsers treat the same unknown field differently
- An unexpected type reaches a handler that does not validate as strictly
- The same bytes produce different results under two declared types

## Patterns

**1. Parser table**

```text
declared type | status | parser | unknown field | validated
application/json | 200 | json | rejected | yes
absent | 200 | fallback | accepted | no  <- finding
text/plain | 415 | none | n/a | n/a
```

**2. Bytes-identical rule**

```text
hold body bytes constant across cases so the only variable is the header the framework reads
```

**3. Client-reality column**

```text
rank each row by whether a real client produces it; a case no client can produce is lower risk, not zero risk
```

## Pitfalls

- Changing the body along with the header, which destroys attribution
- Ranking a fallback path as critical when no client can trigger it, or as harmless when any client can
- Missing that the fallback parser applies a different unknown-field policy

## Done when

- Every accepted and absent content type has a status, parser and validation outcome recorded
- Each row notes whether a real client can produce that case

## References

- [CWE-436 - Interpretation conflict](https://cwe.mitre.org/data/definitions/436.html)
- [IETF RFC 9110 - Content-Type semantics](https://www.rfc-editor.org/rfc/rfc9110)
