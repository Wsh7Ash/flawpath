---
name: parameter-provenance-map
description: "Trace every field the handler reads back to where it comes from, because the field that reaches an assignment without validation is the one a defect is built from. Use when handlers accept input from several sources and no map records which fields arrive from which"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, parameters, provenance]
---

# Parameter Provenance Map

> Trace every field the handler reads back to where it comes from, because the field that reaches an assignment without validation is the one a defect is built from

**Use when:** handlers accept input from several sources and no map records which fields arrive from which

**Avoid when:** one schema defines every input and the source of each field is explicit

## Procedure

1. For each handler, list every field read and mark its source: path, query, header, body or derived server-side.
2. Note where a field is merged from more than one source, since precedence between them is a decision someone made silently.
3. Mark whether each field passes through validation, coercion or sanitization before use, and which of those it gets.
4. Identify fields read from a merged object rather than a named schema, which is where unknown keys survive.
5. Record derived fields separately, since they are computed rather than accepted.
6. Carry unvalidated merged fields into the probe phase as the primary candidates.

## Signals

- A handler reads a merged object rather than a named schema
- Two sources supply the same field with no documented precedence
- A field reaches an assignment with no validation step on its path
- A header-derived value is used where a body field was expected

## Patterns

**1. Provenance row**

```text
field | source | validated | coerced | merged | handler use
id | path | yes | yes | no | lookup
role | body | no | no | yes  <- candidate | assignment
x-tenant | header | no | no | no | routing
```

**2. Merge flag**

```text
any field arriving through a merged object is marked, because unknown keys survive a merge that a named schema would reject
```

**3. Precedence note**

```text
when two sources supply one field, record which wins and where that rule is written, or mark it as an implicit decision
```

## Pitfalls

- Assuming a field is validated because it appears in documentation
- Mapping only body fields and missing header-derived values that affect routing
- Recording derived fields as accepted input, which sends the probe phase after them

## Done when

- Every field read by each handler has a source and a validation status
- Merged and multi-source fields are marked, with precedence recorded or flagged as implicit

## References

- [OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-915 - Improperly controlled modification of dynamically-determined object attributes](https://cwe.mitre.org/data/definitions/915.html)
