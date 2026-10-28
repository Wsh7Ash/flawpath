---
name: integration-and-async-surface-map
description: "Catalogue the queues, webhooks and background jobs a request can trigger, because the effect of a defect often lands off the request path where nobody is watching. Use when a handler can enqueue work or call another service and the reachable side effects have not been listed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, async, integration]
---

# Integration and Async Surface Map

> Catalogue the queues, webhooks and background jobs a request can trigger, because the effect of a defect often lands off the request path where nobody is watching

**Use when:** a handler can enqueue work or call another service and the reachable side effects have not been listed

**Avoid when:** handlers are synchronous and the owner confirms no downstream work is triggered

## Procedure

1. Trace each mutating handler to the jobs, messages or outbound calls it can enqueue, reading the code rather than a diagram.
2. Record what each downstream consumer does with the payload it receives, since that is where an unvalidated field becomes an effect.
3. Note whether a job payload is re-validated on the consuming side or trusted as sent.
4. Identify retry behaviour on each queue, because a retried job multiplies any unintended effect.
5. Mark which downstream systems sit outside your testing boundary, so their behaviour is described rather than exercised.
6. Carry the map into the probe phase with the boundary annotation attached to every out-of-boundary consumer.

## Signals

- A handler enqueues a payload that the consumer parses without re-validating
- A queue retries a malformed message instead of dead-lettering it
- A downstream consumer sits outside the testing boundary but receives data from an in-scope handler
- No one can say what a background job does with the fields it is given

## Patterns

**1. Trigger row**

```text
handler | job or queue | payload fields | consumer re-validates | retries | in scope
PATCH /orders | order.sync | id, status, vendor_ref | no | 5 | vendor is out of boundary
```

**2. Boundary flag**

```text
any consumer outside the boundary is marked describe-only; its behaviour is reported from documentation and code, never exercised
```

**3. Multiplier note**

```text
retry count times one unintended effect is the real impact, so both numbers appear on the row
```

## Pitfalls

- Testing only the request path while the effect lands in a queue nobody is watching
- Describing a downstream system without noting it was never exercised
- Missing that the consumer trusts a payload the in-scope handler never validated

## Done when

- Every mutating handler has a row naming its downstream consumers, payload, re-validation and retries
- Consumers outside the testing boundary are marked describe-only with that reason

## References

- [OWASP - API security guidance](https://owasp.org/API-Security/)
- [CWE-918 - Server-side request forgery](https://cwe.mitre.org/data/definitions/918.html)
