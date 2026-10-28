---
name: api-assessment-boundary
description: "Write down which paths, methods, roles and write operations the backend assessment may exercise, before the first request leaves the workstation. Use when a backend API assessment is about to start and no written list states permitted paths, methods or write operations"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, authorization, rules-of-engagement]
---

# API Assessment Boundary

> Write down which paths, methods, roles and write operations the backend assessment may exercise, before the first request leaves the workstation

**Use when:** a backend API assessment is about to start and no written list states permitted paths, methods or write operations

**Avoid when:** the program publishes a machine-readable endpoint list with permitted methods and a stated rate ceiling

## Procedure

1. Collect the signed rules of engagement, the published API documentation and any internal endpoint list, noting versions used.
2. List every permitted path, method and environment exactly as written, without normalizing or guessing wildcards.
3. Record which write operations are permitted, which are forbidden, and what rollback exists for the permitted ones.
4. Capture the numeric rate ceiling per endpoint and the total request budget for the session.
5. Confirm whether destructive verbs such as delete or purge are permitted at all, since that single answer shapes the whole plan.
6. Save the boundary beside the evidence so a reviewer can prove every recorded request fell inside the permitted set.

## Signals

- Rules list hosts but say nothing about which methods may be sent
- No rate ceiling exists as a number anywhere in the document
- Destructive verbs are neither explicitly allowed nor explicitly banned
- A previous session recorded requests against a path you cannot find in writing

## Patterns

**1. Boundary record**

```text
scope:
  paths: [/api/v1/orders/**, /api/v1/users/me]
  methods: [GET, POST, PATCH]
  forbidden: [DELETE, PUT]
  rate_rps: 2
  writes: create + update allowed, rollback documented
  environments: staging only
```

**2. Pre-flight echo**

```text
Before session start, restate paths, methods, write permissions, rate ceiling and the ban list. Any element you cannot quote is a gap to resolve, not a permission to assume.
```

**3. Evidence binding**

```text
Store boundary.md beside evidence/ so each recorded request line carries a document version it can be checked against during review.
```

## Pitfalls

- Reading a wildcard path as permission for every method on it
- Assuming staging and production share a method list
- Treating an old approval as current after the API changed version

## Done when

- A written boundary table names paths, methods, write permissions, rate ceiling and the ban list
- Every later evidence entry carries the document version that justified the request

## References

- [OWASP - API security testing guidance](https://owasp.org/API-Security/)
- [PortSwigger - Web service testing](https://portswigger.net/web-security)
