---
name: ordering-and-pagination-boundary
description: "Push ordering and pagination to their edges, because an unbounded page or an orderable column is both a resource question and a way to read rows the default view hides. Use when an endpoint returns a list that supports pagination or ordering parameters"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, pagination, resources]
---

# Ordering and Pagination Boundary

> Push ordering and pagination to their edges, because an unbounded page or an orderable column is both a resource question and a way to read rows the default view hides

**Use when:** an endpoint returns a list that supports pagination or ordering parameters

**Avoid when:** limits are clamped server-side and a test confirms out-of-range values are refused

## Procedure

1. Record the default page size and ordering the endpoint applies with no parameters.
2. Request a page size above the maximum and record whether it is clamped, rejected or honoured.
3. Request an offset or cursor beyond the end of the data and record the response rather than assuming one.
4. Try ordering by a column that is not documented as orderable, including an internal or joined field.
5. Measure the response time for an extreme page size against the baseline you already captured.
6. Record limits, clamping and orderable columns with the timing you observed.

## Signals

- An out-of-range page size is honoured instead of clamped
- Ordering by an undocumented or joined column succeeds
- An out-of-range offset returns a different error shape than a bad parameter
- Response time grows sharply with page size beyond what the baseline suggests

## Patterns

**1. Boundary table**

```text
parameter | default | extreme sent | result
page_size | 20 | 100000 | honoured, 2.4s baseline 0.2s
offset | 0 | 999999999 | empty 200
sort | created_at | internal_score | accepted
```

**2. Clamp-versus-reject**

```text
record which behaviour applies: clamp is usually acceptable, honour is the finding, reject is strictest
```

**3. Timing note**

```text
extreme values get a timing recorded against the baseline, since an unbounded page is partly a resource finding
```

## Pitfalls

- Reporting only the pagination logic while the ordering parameter exposes a joined column
- Testing one extreme and missing both the clamp and the reject behaviours
- Quoting a slow response without the baseline it was compared against

## Done when

- Page size, offset and sort each have an extreme-value result with a recorded outcome
- Clamp, reject or honour is stated per parameter with timing against baseline

## References

- [OWASP - API4 unrestricted resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [CWE-770 - Allocation of resources without limits](https://cwe.mitre.org/data/definitions/770.html)
