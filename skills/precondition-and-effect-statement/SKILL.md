---
name: precondition-and-effect-statement
description: "State what an attacker would already need and what changes once they have it, because a defect that requires an existing privilege is a different finding from one that needs none. Use when a confirmed observation is ready to be written up and its severity has not been argued"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [confirm, impact, severity]
---

# Precondition and Effect Statement

> State what an attacker would already need and what changes once they have it, because a defect that requires an existing privilege is a different finding from one that needs none

**Use when:** a confirmed observation is ready to be written up and its severity has not been argued

**Avoid when:** the observation is a configuration note with no behavioural consequence

## Procedure

1. List the precondition: authentication, a role, a valid identifier, or nothing at all.
2. State the effect in terms of what changes in the system, not in adjectives.
3. State what remains impossible even with the behaviour, so the reader sees the claim's boundary.
4. Separate defects with different preconditions into different statements rather than merging them.
5. Rank against a recognized class such as mass assignment, resource exhaustion or information disclosure, with a reason.
6. Write the paragraph a reviewer would accept: precondition, effect, boundary, class, nothing beyond it.

## Signals

- The impact statement is an adjective list with no precondition named
- Severity is stated without saying what an attacker must already possess
- The statement does not say what the behaviour cannot achieve
- Two defects with different preconditions are merged into one claim

## Patterns

**1. Impact skeleton**

```text
precondition: <what the caller must already have>
effect: <what changes in the system>
boundary: <what remains impossible>
class: <mass assignment | resource exhaustion | disclosure | workflow>
```

**2. Worked example**

```text
precondition: authenticated member with an update grant; effect: an undeclared field is stored and read back by later queries; boundary: no cross-tenant read is possible; class: mass assignment
```

**3. Split rule**

```text
if two observations have different preconditions, write two statements; merging them hides the difference a triager needs
```

## Pitfalls

- Claiming critical severity for behaviour that already requires an existing grant
- Omitting the boundary, which makes a reviewer trust the claim less rather than more
- Blending an information disclosure into a state-change finding so neither can be triaged

## Done when

- The statement names precondition, effect, boundary and class in that order
- Observations with different preconditions appear as separate claims

## References

- [OWASP - Risk rating methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)
- [CVSS - Qualitative severity mapping](https://www.first.org/cvss/)
