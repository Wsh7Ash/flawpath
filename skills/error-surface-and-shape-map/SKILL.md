---
name: error-surface-and-shape-map
description: "Catalogue which layer produces each error shape, so a later probe can tell an application rejection from a framework default from a gateway response. Use when error responses have not been attributed to the layer that generates them"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, errors, responses]
---

# Error Surface and Shape Map

> Catalogue which layer produces each error shape, so a later probe can tell an application rejection from a framework default from a gateway response

**Use when:** error responses have not been attributed to the layer that generates them

**Avoid when:** one error formatter handles every response and its output is documented

## Procedure

1. Trigger a small set of controlled errors: not found, bad input, unauthorized, and one rate limit if reachable.
2. Record the status, shape and headers of each, noting whether the body carries a stack or a code.
3. Attribute each shape to a layer: gateway, framework, application or a debug handler.
4. Check whether an error's shape changes when debug mode is on, which the environment delta should already record.
5. Note whether error shapes leak field names, query structure or internal identifiers.
6. Record the map beside the boundary so later probes can be read against it without re-deriving a baseline.

## Signals

- One error carries a stack trace while another of the same status does not
- Error shapes differ by layer and nobody can say which layer produced which
- An error body names internal fields or a query structure
- The shape changes between environments because of a debug setting

## Patterns

**1. Shape map**

```text
condition | status | shape | layer | leaks
unknown id | 404 | {error} | application | no
bad body | 400 | framework default | framework | field names
unhandled | 500 | stack | debug handler | trace
```

**2. Layer attribution**

```text
each shape is attributed to the layer that produced it, with the evidence: headers, shape and environment setting
```

**3. Baseline note**

```text
the map is the baseline later probes compare against; without it a new error cannot be recognised as new
```

## Pitfalls

- Reporting an error shape produced by a debug setting as a production behaviour
- Comparing shapes across environments and attributing the difference to the application
- Recording shapes without the layer, which leaves the fix assigned to nobody

## Done when

- Each triggered error has a recorded status, shape, producing layer and leakage assessment
- The map is stored as the baseline later probes compare against

## References

- [OWASP - Error handling guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-209 - Generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)
