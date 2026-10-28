---
name: response-field-exposure-map
description: "Record which fields each endpoint returns, because an extra field in a response is an exposure that no input-side check will ever catch. Use when response bodies have not been catalogued and over-exposure is a concern for this API"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, responses, exposure]
---

# Response Field Exposure Map

> Record which fields each endpoint returns, because an extra field in a response is an exposure that no input-side check will ever catch

**Use when:** response bodies have not been catalogued and over-exposure is a concern for this API

**Avoid when:** a response schema is enforced and tested for every endpoint

## Procedure

1. Capture the field set each endpoint returns for a record you created, without recording the values.
2. Compare that field set with what the endpoint's documentation says it returns.
3. Mark fields present but undocumented, and fields that reveal internal structure such as roles or flags.
4. Note whether fields vary by role, since a field shown only to administrators tells you its sensitivity.
5. Check for fields derived from joined tables that were never intended to leave the service.
6. Carry undocumented fields into the probe phase as exposure candidates with their endpoint and role noted.

## Signals

- A response contains fields absent from the documented schema
- An internal flag or role field appears in a response for a normal caller
- Fields differ between roles in a way nothing documents
- A joined record's fields appear nested in a response

## Patterns

**1. Exposure row**

```text
endpoint | role | undocumented fields | derived from
GET /orders/{id} | member | internal_flag, vendor_code | joined vendor record
```

**2. Documented-delta**

```text
returned fields minus documented fields; the delta is the finding, listed by name without values
```

**3. Role-variance note**

```text
same endpoint, two roles, differing field sets: recorded with both sets so the difference is explicit
```

## Pitfalls

- Cataloguing values instead of field names, which puts real data in the report
- Comparing only against one role and missing fields visible to another
- Assuming an undocumented field is harmless because it looks internal

## Done when

- Each endpoint has a field set recorded per role, compared against its documentation
- Undocumented and derived fields are listed by name as exposure candidates

## References

- [OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-200 - Exposure of sensitive information](https://cwe.mitre.org/data/definitions/200.html)
