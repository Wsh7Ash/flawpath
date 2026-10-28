---
name: default-value-override-probe
description: "Attempt to set a field to the value the server assigns by default, because a default that a client can pin is a default the server never actually enforces. Use when server-assigned defaults exist on the write path and client ability to supply them is unconfirmed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, defaults, mass-assignment]
---

# Default Value Override Probe

> Attempt to set a field to the value the server assigns by default, because a default that a client can pin is a default the server never actually enforces

**Use when:** server-assigned defaults exist on the write path and client ability to supply them is unconfirmed

**Avoid when:** defaults are computed after assignment and a test confirms a client value is overwritten

## Procedure

1. List the fields the server assigns by default: status, owner, timestamps and counters.
2. Send an update supplying one of those fields with a value of your choosing on a record you own.
3. Read the object back and record whether your value survived or was overwritten by the default.
4. Test one field where overwriting matters, such as a status or an ownership field.
5. Record which defaults are client-overridable and which are enforced server-side.
6. Note whether an overridable default would change a downstream decision.

## Signals

- A client-supplied status survives where the server normally assigns one
- An ownership or creator field can be pinned to a value the client chose
- A timestamp is accepted from the client rather than generated on the server
- A counter or balance field accepts a client-supplied starting value

## Patterns

**1. Override table**

```text
field | default | client value sent | result
status | draft | active | stored active  <- overridden
created_by | server | other-user | stored other-user
id | server | client-value | rejected
```

**2. Enforcement split**

```text
defaults split into enforced (server wins) and overridable (client wins); the split is the reportable structure
```

**3. Decision check**

```text
for each overridable default, state what downstream decision it would influence, or record it as cosmetic
```

## Pitfalls

- Testing only a cosmetic default while an ownership default is also overridable
- Reporting an overridable field that nothing consumes as though it were a state change
- Not comparing against the enforced defaults, which is what shows the inconsistency

## Done when

- Each default field has a record of client value sent and the stored result
- The enforced and overridable split is stated, with downstream effect noted per field

## References

- [CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)
- [OWASP - Mass assignment guidance](https://owasp.org/www-project-web-security-testing-guide/)
