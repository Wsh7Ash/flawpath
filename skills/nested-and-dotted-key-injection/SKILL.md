---
name: nested-and-dotted-key-injection
description: "Test whether a bracketed or dotted key path reaches a nested field the flat schema does not expose, since a parser that maps key paths can write where the schema never declared anything. Use when the parser accepts a structured body and nested key paths have not been exercised"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, mass-assignment, parsing]
---

# Nested and Dotted Key Injection

> Test whether a bracketed or dotted key path reaches a nested field the flat schema does not expose, since a parser that maps key paths can write where the schema never declared anything

**Use when:** the parser accepts a structured body and nested key paths have not been exercised

**Avoid when:** the parser flattens nothing and a test confirms a dotted key is rejected as unknown

## Procedure

1. Confirm the boundary permits the write and identify the synthetic record you will update.
2. Send an update using a dotted or bracketed key that targets a nested field not in the schema.
3. Read the object back, including its nested structure, and compare against the captured state.
4. Try one alternate notation to see whether the mapping is notation-specific or general.
5. Record which notation reached the nested field, and the path it wrote to.
6. Note whether the flat equivalent of the same field is rejected, since the difference is the finding.

## Signals

- A dotted key writes to a nested field while the flat equivalent is rejected
- Bracket notation reaches a field the schema declares nowhere
- The stored object gains a key containing a literal dot rather than nesting
- A control flat unknown key is rejected while the notated one is accepted

## Patterns

**1. Notation pair**

```text
flat: {internal.flag: true} -> rejected, stored unchanged
bracket: {internal[flag]: true} -> stored under a nested path
```

**2. Read-back rule**

```text
read the whole object including nested keys, because a notation can either nest the value or store a literal dotted key
```

**3. Control note**

```text
the flat unknown key is the control that proves the rejection policy exists for one form but not the other
```

## Pitfalls

- Testing only one notation and concluding the whole class is safe
- Not distinguishing a stored literal dotted key from a nested field
- Omitting the flat control, which is what makes the difference visible

## Done when

- At least two notations are tested with read-back results recorded for each
- A flat control result is recorded alongside the notated attempts

## References

- [CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)
- [OWASP - Input validation guidance](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
