---
name: enum-and-range-boundary-probe
description: "Send values at and just outside each declared enumeration and range, because a boundary enforced on the documented edge but not past it is where an unexpected state enters. Use when fields declare enumerations or numeric ranges that have not been exercised at their edges"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, validation, boundaries]
---

# Enum and Range Boundary Probe

> Send values at and just outside each declared enumeration and range, because a boundary enforced on the documented edge but not past it is where an unexpected state enters

**Use when:** fields declare enumerations or numeric ranges that have not been exercised at their edges

**Avoid when:** the schema enforces bounds strictly and an out-of-range test confirms rejection

## Procedure

1. List enumerated and ranged fields with their documented boundaries.
2. For each, send the maximum in-range value, the value just outside it, and one clearly invalid value.
3. Read the object back and record accepted, rejected or coerced for each case.
4. Check whether an out-of-range value is clamped into range, which silently changes what was requested.
5. For enumerations, test a value that is plausible but undeclared rather than an obviously invalid string.
6. Record a boundary table with one row per field and its three test cases.

## Signals

- A value just outside the documented range is accepted
- An out-of-range value is clamped rather than rejected
- An undeclared but plausible enumeration value is accepted
- The documented boundary differs from the enforced one

## Patterns

**1. Boundary table**

```text
field | declared | max in-range | just outside | invalid
quantity | 1..100 | 100 ok | 101 stored 101 | 0 rejected
state | draft|active|paid | paid ok | refunded accepted | xyz rejected
```

**2. Clamp flag**

```text
a clamped value is recorded separately from an accepted one, because the caller asked for something else than what was stored
```

**3. Plausible-enum rule**

```text
test an undeclared value that looks legitimate, since a clearly invalid string is usually caught by the most basic check
```

## Pitfalls

- Testing only a clearly invalid value while the plausible undeclared one passes
- Recording a clamp as an acceptance, which hides that stored state differs from the request
- Not comparing the documented boundary with the enforced one

## Done when

- Each enumerated or ranged field has three boundary cases with a result
- Clamped values are distinguished from accepted ones in the table

## References

- [CWE-1284 - Improper validation of specified quantity in input](https://cwe.mitre.org/data/definitions/1284.html)
- [OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
