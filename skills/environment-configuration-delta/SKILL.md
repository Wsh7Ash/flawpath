---
name: environment-configuration-delta
description: "Record which settings differ between the environment you test and the one that matters, because a check passing in staging says nothing about production behaviour. Use when the assessment runs against a non-production environment while findings will apply to production"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, configuration, environment]
---

# Environment Configuration Delta

> Record which settings differ between the environment you test and the one that matters, because a check passing in staging says nothing about production behaviour

**Use when:** the assessment runs against a non-production environment while findings will apply to production

**Avoid when:** one environment serves all traffic and configuration is identical by construction

## Procedure

1. List the settings that govern behaviour: validation strictness, debug mode, authentication enforcement, rate limits and feature flags.
2. Read each value in the tested environment and record it verbatim beside the documented production value.
3. Flag any setting where the tested environment is more permissive than production, or the reverse.
4. Note feature flags that change which code path runs, since a flag difference makes a finding inapplicable.
5. State in the report which findings depend on a setting that differs between environments.
6. Keep the delta current, since configuration changes while an assessment runs.

## Signals

- Debug mode or verbose errors are enabled in the environment you are testing
- Validation strictness differs between the tested and production settings
- A feature flag routes one environment to a different handler
- The delta has never been read, so findings are assumed transferable

## Patterns

**1. Delta row**

```text
setting | tested env | production | effect on findings
debug | on | off | error-shape findings not transferable
strict validation | off | on | coercion findings may not apply
```

**2. Transfer statement**

```text
for each finding, one line saying whether it depends on a differing setting, so a reader knows which to re-verify in production
```

**3. Flag note**

```text
feature flags that change routing are recorded with their state, because a flag-off path was never exercised
```

## Pitfalls

- Reporting a debug-only error shape as a production defect
- Assuming staging is stricter than production when the opposite is true
- Noting a flag difference but never stating which findings it invalidates

## Done when

- A delta table lists each behavioural setting in both environments with its effect on findings
- Findings that depend on a differing setting are marked transferable or not

## References

- [OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- [NIST SP 800-53 - Configuration settings controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
