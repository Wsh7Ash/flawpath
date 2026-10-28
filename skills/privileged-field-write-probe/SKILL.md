---
name: privileged-field-write-probe
description: "Attempt to set one field that the role matrix reserves for another role, using a single field change so the result can be attributed to exactly that field. Use when the state map identifies fields reserved for a role you are not testing as, and the write is permitted by the boundary"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, authorization, mass-assignment]
---

# Privileged Field Write Probe

> Attempt to set one field that the role matrix reserves for another role, using a single field change so the result can be attributed to exactly that field

**Use when:** the state map identifies fields reserved for a role you are not testing as, and the write is permitted by the boundary

**Avoid when:** the endpoint is documented to reject reserved fields and a test confirms it

## Procedure

1. Pick one reserved field from the state map and confirm the boundary permits the write method and path.
2. Send an update changing only that one field on a synthetic record you own.
3. Read the record back and record whether the reserved field changed.
4. Compare with a control update that changes only a permitted field, to prove the endpoint accepts writes at all.
5. If the change is rejected, record the rejection's status and shape against the error map baseline.
6. Record a one-field result with both the reserved and control attempts beside it.

## Signals

- A field reserved to another role changes after a single-field update
- The response returns the reserved field as though it were a normal property
- Rejection uses a generic validation error rather than an authorization one
- The control update and the reserved update behave identically, which is itself informative

## Patterns

**1. Single-field pair**

```text
control: PATCH {nickname: t1} -> 200, nickname changed
reserved: PATCH {role: admin} -> 200, role changed <- finding
```

**2. Attribution rule**

```text
one field per request; a request changing two fields cannot attribute the outcome to either
```

**3. Rejection class**

```text
a 403 means authorization caught it, a 400 means schema validation caught it, and 200 means neither did; record which occurred
```

## Pitfalls

- Sending several fields at once and being unable to say which one changed the object
- Testing against a record you do not own, which turns a probe into an unauthorized change
- Reading a 400 as an authorization success when it may only be schema validation

## Done when

- A reserved field and a permitted control each have a single-field result recorded
- The rejection class is recorded as authorization, validation, or neither

## References

- [OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-269 - Improper privilege management](https://cwe.mitre.org/data/definitions/269.html)
