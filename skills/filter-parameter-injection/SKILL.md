---
name: filter-parameter-injection
description: "Add a filter or query parameter the endpoint does not document and observe whether it narrows or widens the result set, because an unvalidated filter changes who sees which rows. Use when an endpoint returns a filtered list and its parameter handling has not been exercised"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, filtering, authorization]
---

# Filter Parameter Injection

> Add a filter or query parameter the endpoint does not document and observe whether it narrows or widens the result set, because an unvalidated filter changes who sees which rows

**Use when:** an endpoint returns a filtered list and its parameter handling has not been exercised

**Avoid when:** a strict allow-list of parameters is enforced and a test confirms unlisted ones are rejected

## Procedure

1. Capture a baseline list response for a record set you are allowed to read, noting the count and field set.
2. Add one undocumented filter parameter and record whether the result set changes.
3. Try a filter that would widen access, such as one targeting a tenant or owner field.
4. Record the status, the count delta and whether the parameter appears in the response or an error.
5. Check whether the filter is applied in the query rather than after fetching, since that affects scale behaviour too.
6. Record each parameter with accepted, rejected or ignored as its verdict.

## Signals

- An undocumented filter parameter changes the returned count
- A filter targeting an ownership or tenant field is accepted
- The parameter is applied after rows are fetched rather than in the query
- An invalid filter value produces an error that echoes the query structure

## Patterns

**1. Parameter verdict**

```text
param | value | count before | count after | verdict
(sort unspecified) | default | 20 | 20 | baseline
include_internal | true | 20 | 27 | accepted, widened
owner_id | other | 20 | 0 | accepted, filtered by ownership
```

**2. Widen-versus-narrow**

```text
record whether the parameter widened or narrowed the set; widening is the direction that changes who sees what
```

**3. Application point**

```text
note whether filtering happens in the query or in application code, since a post-fetch filter has a scale consequence as well
```

## Pitfalls

- Adding several parameters at once and losing which one changed the count
- Testing only narrowing filters when widening is the direction that matters
- Missing that a filter changed nothing because the parameter needs a different name

## Done when

- Each undocumented parameter has an accepted, rejected or ignored verdict with count delta
- Whether the filter widens or narrows access is stated per parameter

## References

- [OWASP - API4 unrestricted resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [CWE-639 - Authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)
