---
name: fix-worded-in-framework-terms
description: "Describe each remediation in the vocabulary of the framework and layer that owns it, so the implementer can act without reverse-engineering your finding first. Use when a backend finding is ready to include remediation across handler, middleware and configuration layers"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [document, remediation, communication]
---

# Fix Worded in Framework Terms

> Describe each remediation in the vocabulary of the framework and layer that owns it, so the implementer can act without reverse-engineering your finding first

**Use when:** a backend finding is ready to include remediation across handler, middleware and configuration layers

**Avoid when:** the fix is one configuration value with an obvious verification step

## Procedure

1. Name the layer for each step: request schema, handler, middleware, framework configuration or gateway.
2. Write the step in the framework's own terms, naming the object or setting the implementer will change.
3. State the expected effect so a reader can verify the change rather than assume it.
4. Include a retest instruction using the exact request from the probe that revealed the defect.
5. Mark steps needing a partner action or a scheduled window, since those need coordination rather than a merge request.
6. List what you deliberately did not change and why, so nothing appears silently out of scope.

## Signals

- A remediation step says add validation without naming the object or setting to change
- A step requiring a migration or a window appears with no owner or date
- No retest instruction is given, so closure cannot be verified
- The report does not say which related items were left unchanged

## Patterns

**1. Step line**

```text
layer: request schema | change: declare strict request object rejecting unknown fields | effect: probe now returns uniform 400 | retest: replay evidence E-011
```

**2. Framework vocabulary**

```text
reference the actual object the implementer changes: the schema class, the middleware registration, the setting name, not a general principle
```

**3. Not-changed list**

```text
unchanged: gateway timeout, because it belongs to the platform team; recorded so it is not reported as an outstanding item on our side
```

## Pitfalls

- Writing generic advice the implementer already knows while omitting the specifics of this stack
- Hiding a partner-dependent step inside our own task list so it never gets scheduled
- Omitting retest instructions, which makes an owner's closure claim unverifiable

## Done when

- Every step names its layer, its effect in framework terms and a retest instruction
- Partner-dependent steps carry an owner and a date, and unchanged items are listed with reasons

## References

- [OWASP - Remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-40 - Patch and configuration management](https://csrc.nist.gov/pubs/sp/800/40/r4/final)
