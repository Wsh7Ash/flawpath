---
name: route-verb-matrix
description: "Build the path-by-method matrix from the router itself, because an undocumented method on a documented path is usually where the newest and least-reviewed handler lives. Use when a route inventory exists but has not been expanded into a full path-by-method matrix"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, routes, methods]
---

# Route Verb Matrix

> Build the path-by-method matrix from the router itself, because an undocumented method on a documented path is usually where the newest and least-reviewed handler lives

**Use when:** a route inventory exists but has not been expanded into a full path-by-method matrix

**Avoid when:** framework-generated documentation already lists every path with every method and its handler

## Procedure

1. Read the router table and expand it into one row per path and method combination actually registered.
2. Mark each cell as documented or undocumented, and as having middleware or none.
3. Probe for a method the matrix does not list on a path you expect to answer, such as an override or a fallback.
4. Note framework defaults, such as an automatically registered index or an options handler.
5. Check for method override handling where a body or header field changes the effective verb.
6. Carry undocumented cells into the probe phase as the highest-value handlers to examine.

## Signals

- A path answers a method the matrix does not list
- A method override field or header changes which handler runs
- An automatically registered fallback handler exists with no middleware
- One path has three methods while its neighbours have one each

## Patterns

**1. Matrix row**

```text
path | method | handler | middleware | documented
/api/v1/orders | GET | list | auth | yes
/api/v1/orders | PATCH | update | auth | yes
/api/v1/orders | DELETE | destroy | none | no  <- undocumented
```

**2. Override check**

```text
send a permitted method with an override field set to a forbidden verb and observe whether the handler changes; a change means the matrix must record effective verbs
```

**3. Fallback flag**

```text
an automatically registered handler gets its own row with a flag, because nobody reviewed it when it was added
```

## Pitfalls

- Building the matrix from documentation, which is what drifted in the first place
- Recording only the documented verb and never probing for an undocumented one
- Missing a method override that makes the effective verb different from the sent one

## Done when

- Every path has one row per registered method with middleware and documentation status
- At least one probe for an unlisted method or override has a recorded result

## References

- [OWASP - API9 Improper inventory management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)
- [CWE-778 - Insufficient logging](https://cwe.mitre.org/data/definitions/778.html)
