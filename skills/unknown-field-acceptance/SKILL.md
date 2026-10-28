---
name: unknown-field-acceptance
description: "Send a field the schema never declares and see whether it survives to the stored object, because acceptance is the precondition every mass-assignment defect needs. Use when the boundary permits write requests and the parser's unknown-field policy has not been exercised"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, mass-assignment, validation]
---

# Unknown Field Acceptance

> Send a field the schema never declares and see whether it survives to the stored object, because acceptance is the precondition every mass-assignment defect needs

**Use when:** the boundary permits write requests and the parser's unknown-field policy has not been exercised

**Avoid when:** the parser demonstrably rejects unknown fields and a test confirms it in the current build

## Procedure

1. Confirm the boundary permits the write and that a rollback exists for the record you will use.
2. Create or select a synthetic record you own and capture its state before the request.
3. Send an update containing one field name the schema does not declare, alongside a permitted field.
4. Read the record back and compare field set and values against the captured state.
5. Repeat with a second unknown name to separate a name-specific rejection from a general policy.
6. Record acceptance or rejection with the before and after state, never the sensitive value itself.

## Signals

- An undeclared field appears on the stored object after the update
- The response echoes the undeclared field as though it were part of the schema
- A second unknown name is also accepted, indicating a policy rather than an exception
- The field is stored but not returned, which still means it was accepted

## Patterns

**1. Before and after**

```text
before: {status: draft, owner: me}
request: {status: active, internal_marker: true}
after: {status: active, internal_marker: true} <- unknown accepted
```

**2. Two-name rule**

```text
send two different unknown names; both accepted means the parser passes unknown keys through by policy
```

**3. Stored-not-returned**

```text
field absent from the response but present on read-back still counts as accepted; record the read-back as the evidence
```

## Pitfalls

- Judging acceptance from the response body alone when the field is stored but not echoed
- Changing two known fields at once, which makes an unknown field's effect impossible to isolate
- Using a record you do not own and leaving it modified

## Done when

- Two unknown names each have a recorded before and after state
- Acceptance is determined from read-back rather than from the response body

## References

- [OWASP - Mass assignment guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)
