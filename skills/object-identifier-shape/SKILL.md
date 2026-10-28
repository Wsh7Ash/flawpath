---
name: object-identifier-shape
description: "Characterise how object identifiers are formed and whether they are predictable, because the shape decides whether an authorization check is doing real work or just matching a guessable key. Use when endpoints address domain objects by an identifier and its formation has not been recorded"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, identifiers, authorization]
---

# Object Identifier Shape

> Characterise how object identifiers are formed and whether they are predictable, because the shape decides whether an authorization check is doing real work or just matching a guessable key

**Use when:** endpoints address domain objects by an identifier and its formation has not been recorded

**Avoid when:** identifiers are documented as opaque and confirmed non-enumerable by construction

## Procedure

1. Collect identifier examples from responses, replacing values with their structural properties only.
2. Classify the shape: sequential integer, time-ordered, random fixed length, composite key or a hash.
3. Record whether an identifier appears in a location a client can influence, such as a query or a header.
4. Check whether authorization is checked against the identifier's owner, or only that the object exists.
5. Note whether enumeration would be observable in rate limits or logs, since that bounds the practical risk.
6. Carry the shape and its authorization treatment into the probe phase together, not separately.

## Signals

- Identifiers are sequential integers across a tenant boundary
- An identifier appears in a response for an object the caller does not own
- The check verifies existence but not ownership of the returned object
- No rate limit or log line would reveal an enumeration pattern

## Patterns

**1. Shape record**

```text
shape: sequential integer | exposed in: response body, path | ownership checked: yes (separate query) | enumeration observable: yes via 404 timing
```

**2. Authorization pairing**

```text
record identifier shape next to the authorization check; a guessable identifier with an existence-only check is the pairing that matters
```

**3. Client-influence note**

```text
whether a client can supply the identifier in a header or query changes who controls the lookup
```

## Pitfalls

- Recording the identifier shape without the authorization treatment, which is the other half of the finding
- Calling a random-looking identifier safe without reading the check that uses it
- Ignoring that an existence check still reveals whether an object exists

## Done when

- Every identifier class has a recorded shape, exposure locations and authorization treatment
- Whether enumeration would be observable in rate limits or logs is stated

## References

- [OWASP - API1 broken object level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [CWE-330 - Use of insufficiently random values](https://cwe.mitre.org/data/definitions/330.html)
