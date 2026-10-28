---
name: environment-transferability-check
description: "Re-read the environment delta and mark each finding as transferable or not, so a defect that only exists behind a staging flag never reaches production as a claim. Use when findings were established in one environment and are about to be reported against another"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [confirm, environment, reporting]
---

# Environment Transferability Check

> Re-read the environment delta and mark each finding as transferable or not, so a defect that only exists behind a staging flag never reaches production as a claim

**Use when:** findings were established in one environment and are about to be reported against another

**Avoid when:** one environment serves all traffic and configuration is identical by construction

## Procedure

1. Re-read the environment delta table, since configuration may have changed since the assessment began.
2. For each finding, identify which settings it depends on, if any.
3. Mark the finding transferable, not transferable, or unknown, with the setting responsible.
4. For unknown, state what would settle it: a reading, a test in the other environment, or an owner's answer.
5. Re-check any finding that depended on a debug flag or a validation mode, since those differ most often.
6. Place the transferability column beside each finding rather than in an appendix.

## Signals

- A finding's transferability was never assessed against the delta
- A debug-flag-dependent error shape is reported as a production behaviour
- Transferability is discussed once in general terms rather than per finding
- The delta has not been re-read since the assessment started

## Patterns

**1. Transfer column**

```text
finding | depends on setting | tested env | production | transferable
F-01 | validation strictness | off | on | no
F-02 | nothing | - | - | yes
```

**2. Unknown handling**

```text
unknown -> state what settles it: a config reading, a test in that environment, or an owner's written answer
```

**3. Placement rule**

```text
the column sits beside the finding so a reader meets it before acting, never in an appendix
```

## Pitfalls

- Assuming transferability for all findings with one sentence at the top of the report
- Reporting a debug-only shape as a production defect
- Marking a finding transferable without naming the setting it depends on

## Done when

- Every finding has a transferability verdict with the setting responsible or a stated none
- Unknown verdicts state what would settle them, and the column sits beside the findings

## References

- [OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- [NIST SP 800-53 - Configuration settings controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
