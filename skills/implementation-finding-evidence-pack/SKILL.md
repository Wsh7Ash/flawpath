---
name: implementation-finding-evidence-pack
description: "Assemble a report where every implementation claim carries its request pair, response diff, attribution and boundary version, so a reader can check the claim rather than trust it. Use when a confirmed backend observation is ready to be written up for the owning team"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [document, evidence, reporting]
---

# Implementation Finding Evidence Pack

> Assemble a report where every implementation claim carries its request pair, response diff, attribution and boundary version, so a reader can check the claim rather than trust it

**Use when:** a confirmed backend observation is ready to be written up for the owning team

**Avoid when:** the finding has already been reported and only a closing note remains

## Procedure

1. State the defect in one sentence naming endpoint, input and outcome, without adjectives.
2. Attach the baseline and probe captures so the difference is visible rather than described.
3. Include the single-input attribution replay that establishes which input caused the effect.
4. Record the request shapes for both captures, including which field you varied.
5. Give the reproduction recipe and the boundary version that permitted each request.
6. State impact as precondition, effect, boundary and class, and stop there.

## Signals

- A report claims an implementation defect without the request pair that revealed it
- The attribution replay is missing, so the causal claim rests on an assumption
- Statuses are given without the response diff that distinguishes the cases
- Impact is stated without naming the precondition an attacker would already need

## Patterns

**1. Claim skeleton**

```text
claim: <endpoint> stores <undeclared input> because <allow-list> is absent
baseline vs probe: <the diff>
attribution: <input> alone reproduces it
impact: precondition / effect / boundary / class
```

**2. Evidence block**

```text
E-011 | PATCH /orders/{id} | body: {status, extra_field} | resp 200 | read-back: extra_field present | boundary v3
```

**3. Boundary note**

```text
attach the boundary version and mark each request as permitted by it, so the test itself can be audited
```

## Pitfalls

- Presenting a narrative claim when the reader needs the raw request pair to judge it
- Leaving out the attribution replay, which is what makes it a causal claim rather than a correlation
- Inflating impact beyond what the recorded requests demonstrate

## Done when

- Every claim is followed by a baseline and probe pair with the attribution replay
- The reproduction recipe and boundary version are attached to the pack

## References

- [OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-61 - Incident handling guidance](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
