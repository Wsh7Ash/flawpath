---
name: response-differential-comparison
description: "Compare the full response against a baseline capture field by field, so the reported difference is the one that exists rather than the one that caught your eye. Use when a probe produced a response and the report needs an exact statement of what differs"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [confirm, comparison, evidence]
---

# Response Differential Comparison

> Compare the full response against a baseline capture field by field, so the reported difference is the one that exists rather than the one that caught your eye

**Use when:** a probe produced a response and the report needs an exact statement of what differs

**Avoid when:** the response is a simple status with no body structure to compare

## Procedure

1. Capture a baseline response with every input at its normal value, including headers and timing.
2. Capture the probe response under identical conditions except for the single varied input.
3. Diff both captures field by field across status, headers and every body field.
4. Record every difference found, not only the one you were looking for.
5. Attribute each difference to the varied input, or mark it as unattributed and re-test it.
6. Store both captures so a reviewer can repeat the comparison themselves.

## Signals

- Only the expected difference was reported while a second one went unrecorded
- The baseline and the probe capture came from different sessions or environments
- Headers were not compared even though a header changed
- An unattributed difference was dropped rather than re-tested

## Patterns

**1. Diff record**

```text
baseline: status 200, field set {a,b,c}, header x-1
probe:    status 200, field set {a,b,d}, header x-2
differences: c removed, d added, x changed
```

**2. Full-field rule**

```text
report every difference the diff finds; an unremarked second difference is often the more interesting one
```

**3. Re-test loop**

```text
any difference you cannot attribute to the varied input gets its own single-input replay rather than being discarded
```

## Pitfalls

- Reporting only the expected difference and letting a second one pass unnoticed
- Comparing captures taken under different conditions, which introduces noise into the claim
- Discarding an unattributed difference instead of testing it separately

## Done when

- Baseline and probe captures are diffed field by field with every difference recorded
- Each difference is attributed to an input or re-tested on its own

## References

- [NIST - Evidence handling guidance](https://csrc.nist.gov/publications/detail/sp/800-86/final)
- [OWASP - Testing methodology](https://owasp.org/www-project-web-security-testing-guide/)
