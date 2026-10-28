---
name: idempotency-key-handling
description: "Replay one request with the same idempotency key and compare the effects, because a key that is recorded but not enforced produces a duplicate every retry. Use when the API accepts an idempotency key or a client-generated identifier for a create operation"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, idempotency, concurrency]
---

# Idempotency Key Handling

> Replay one request with the same idempotency key and compare the effects, because a key that is recorded but not enforced produces a duplicate every retry

**Use when:** the API accepts an idempotency key or a client-generated identifier for a create operation

**Avoid when:** a test confirms a replayed key returns the original result without a second effect

## Procedure

1. Confirm the boundary permits the create operation and identify its rollback.
2. Send a create with a client-generated key and record the response and the created record.
3. Replay the identical request with the same key and record the response and any second record.
4. Compare the two responses and the resulting object count to determine whether the effect repeated.
5. Send a third request with the same key but a changed body to see which of the two the server honours.
6. Record the key's behaviour: enforced, recorded but not enforced, or ignored.

## Signals

- A replay with the same key creates a second object
- The key is recorded in logs or responses but does not suppress the effect
- A changed body with a reused key is processed rather than rejected
- The response to a replay differs from the original with no explanation

## Patterns

**1. Replay record**

```text
request 1 key K -> 201, object A
request 2 key K same body -> 201, object B  <- effect repeated
request 3 key K changed body -> 201, object C
```

**2. Three-request rule**

```text
the third request with a changed body is what distinguishes a key that is ignored from one that is enforced but keyed only on the body
```

**3. Count evidence**

```text
object count after each replay is the evidence; record it beside the status codes rather than relying on status alone
```

## Pitfalls

- Judging enforcement from the status code when a second object was created anyway
- Replaying a request the boundary forbids for this operation
- Skipping the changed-body case, which is what separates ignored from enforced

## Done when

- Three requests with one key have recorded responses and object counts
- The key is labelled enforced, recorded but not enforced, or ignored

## References

- [CWE-841 - Improper enforcement of behavioral workflow](https://cwe.mitre.org/data/definitions/841.html)
- [OWASP - Race condition guidance](https://owasp.org/www-project-web-security-testing-guide/)
