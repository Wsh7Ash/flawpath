---
name: single-input-attribution
description: "Prove that exactly one input caused the observed outcome by replaying with only that input changed, because a multi-field request cannot support a causal claim. Use when a probe changed several inputs at once and the report needs to say which one mattered"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [confirm, attribution, method]
---

# Single-Input Attribution

> Prove that exactly one input caused the observed outcome by replaying with only that input changed, because a multi-field request cannot support a causal claim

**Use when:** a probe changed several inputs at once and the report needs to say which one mattered

**Avoid when:** the original probe already varied exactly one input

## Procedure

1. List every input the original request changed relative to its baseline.
2. Replay with all inputs at baseline except one candidate, which is the only value you vary.
3. Record whether the outcome reproduces; if not, move to the next candidate.
4. Continue until one input alone reproduces the outcome or none does.
5. When none alone reproduces it, record that the effect is combinatorial rather than picking a single cause.
6. Write the attribution as one input with its replay result, or as a combination with the members named.

## Signals

- A request changed three fields and the report attributes the effect to one of them without a replay
- No single input reproduces the effect when tested alone
- The attribution rests on which field seemed most plausible
- A baseline replay was never performed against the original request

## Patterns

**1. Attribution replay**

```text
original: {a:1, b:2, c:3} -> outcome
replay: {a:1, base, base} -> outcome reproduced -> a is the cause
```

**2. Combinatorial case**

```text
no single input reproduces it -> record the combination, name its members, and say the effect requires them together
```

**3. Baseline-first rule**

```text
always replay the baseline first to confirm the outcome was not incidental to the environment
```

## Pitfalls

- Naming a cause because it looks most plausible rather than because it reproduces the effect
- Stopping at the first input that correlates instead of testing each in isolation
- Never replaying the baseline, so an environmental change could explain the outcome

## Done when

- Exactly one input, or a named combination, is recorded with the replay that isolates it
- A baseline replay confirms the outcome was not environmental

## References

- [NIST - Evidence-based assessment practice](https://csrc.nist.gov/publications/detail/sp/800-86/final)
- [OWASP - Testing methodology](https://owasp.org/www-project-web-security-testing-guide/)
