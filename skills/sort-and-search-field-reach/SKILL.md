---
name: sort-and-search-field-reach
description: "Check which fields sorting and free-text search can reach, since a search over a field the list never shows returns rows the caller was never meant to select. Use when the endpoint supports a search term or a sort field and the reachable column set is unconfirmed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, search, exposure]
---

# Sort and Search Field Reach

> Check which fields sorting and free-text search can reach, since a search over a field the list never shows returns rows the caller was never meant to select

**Use when:** the endpoint supports a search term or a sort field and the reachable column set is unconfirmed

**Avoid when:** search and sort operate over a documented field allow-list enforced server-side

## Procedure

1. Capture a baseline result set for a search term that matches nothing, so the empty state is known.
2. Search for a value that exists only in a field the response never returns and record whether rows come back.
3. Sort by an undocumented field and record whether ordering changes as evidence the field was used.
4. Check whether an error from a malformed sort or search term leaks column or query detail.
5. Compare the searched field set against the response field set from the exposure map.
6. Record each searched or sorted field with reachable, rejected or ignored as its verdict.

## Signals

- Searching a hidden field returns rows, proving the field is reachable
- Sorting by an undocumented column changes the result order
- A malformed sort term produces an error naming a column or a query fragment
- Search reaches fields outside the response schema entirely

## Patterns

**1. Reach verdict**

```text
field | in response | searchable | sortable | evidence
email | no | yes | no | rows returned for known value
internal_score | no | no | yes | order changed
```

**2. Baseline empty**

```text
a term matching nothing gives the empty-state shape, which is what a later error or leak is compared against
```

**3. Error check**

```text
a malformed sort term that names a column in its error is recorded as disclosure in its own right
```

## Pitfalls

- Testing search while never checking sort, which often reaches further
- Recording a leak without the baseline empty response to show the error is new
- Assuming a field is unreachable because it is absent from the response

## Done when

- Each searched and sorted field has a reachable, rejected or ignored verdict with evidence
- A baseline empty-result response exists for comparison against errors

## References

- [OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-200 - Exposure of sensitive information](https://cwe.mitre.org/data/definitions/200.html)
