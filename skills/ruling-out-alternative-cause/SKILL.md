---
name: ruling-out-alternative-cause
description: "Name the other explanations for what you saw and test each one, because a finding that survives every alternative is the only kind that survives review. Use when an observation is confirmed and at least one other cause could plausibly explain it"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [confirm, method, rigour]
---

# Ruling Out Alternative Cause

> Name the other explanations for what you saw and test each one, because a finding that survives every alternative is the only kind that survives review

**Use when:** an observation is confirmed and at least one other cause could plausibly explain it

**Avoid when:** the single-input replay already rules out every plausible alternative by construction

## Procedure

1. List the alternative causes: client-side caching, an environment setting, a concurrent writer, a gateway rewrite or your own tooling.
2. For each alternative, design the one observation that would distinguish it from the finding you intend to report.
3. Run those distinguishing observations and record the result for each.
4. Mark each alternative ruled out with its evidence, or ruled in, which changes the finding entirely.
5. Where an alternative cannot be ruled out with the access you have, say so plainly in the report.
6. Keep the alternatives list with the finding, since a reviewer will ask the same questions.

## Signals

- A plausible alternative was never tested before the claim was written
- Your own tooling could explain the observation and was not checked
- An alternative was dismissed in prose rather than by an observation
- An untestable alternative is absent from the report as though it did not exist

## Patterns

**1. Alternative table**

```text
alternative | distinguishing test | result | verdict
client cache | bypass client cache | same outcome | ruled out
staging flag | read setting | differs from prod | ruled in, finding transferable: no
```

**2. Unsettleable case**

```text
alternative that cannot be tested with your access -> written as an open alternative in the report, not omitted
```

**3. Own-tooling check**

```text
first alternative to test is your own client, since it is both the most likely and the cheapest to rule out
```

## Pitfalls

- Asserting an alternative is impossible without an observation that shows it
- Forgetting that your own tooling may add caching, headers or retries
- Omitting an untestable alternative, which makes the claim look stronger than it is

## Done when

- Every plausible alternative has a distinguishing test with a recorded result
- Any alternative that cannot be ruled out is stated in the report as an open one

## References

- [NIST - Evidence-based assessment practice](https://csrc.nist.gov/publications/detail/sp/800-86/final)
- [OWASP - Testing methodology](https://owasp.org/www-project-web-security-testing-guide/)
