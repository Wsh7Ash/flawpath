---
name: middleware-chain-order
description: "Read the middleware chain in the order it actually executes, because a validation step that runs after authorization changes what an unauthenticated caller can reach. Use when middleware is applied at several layers and its real execution order has not been read from configuration"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [map, middleware, order]
---

# Middleware Chain Order

> Read the middleware chain in the order it actually executes, because a validation step that runs after authorization changes what an unauthenticated caller can reach

**Use when:** middleware is applied at several layers and its real execution order has not been read from configuration

**Avoid when:** one documented chain applies to every route and the code confirms it

## Procedure

1. Read the chain from the router or application setup and write the steps in execution order.
2. Mark which steps are global, which are per-route and which apply only to a path prefix.
3. Note where a step can be skipped, such as an optional authentication handler that passes on failure.
4. Identify ordering dependencies: validation before use, authorization before handler, rate limiting before work.
5. Check whether any step short-circuits the chain or falls through to the handler on error.
6. Record deviations from the documented order as findings about configuration rather than about code.

## Signals

- Authorization is registered after a body-parsing step
- An authentication handler falls through to the handler when verification fails
- A per-route chain omits a global step rather than extending it
- The configured order differs from the documented order

## Patterns

**1. Chain record**

```text
1 rate-limit  2 cors  3 authenticate  4 authorize  5 parse  6 validate  7 handler
read from configuration, not from documentation
```

**2. Skip-path flag**

```text
each step that can be skipped or that falls through on failure is marked, since a silent fallthrough is the defect shape
```

**3. Deviation note**

```text
configured vs documented order, with the file that holds the configured one, so the fix has a location
```

## Pitfalls

- Trusting the documented chain instead of the one the configuration builds
- Checking that a step exists without reading where it sits in the order
- Missing that a per-route chain replaces the global chain rather than extending it

## Done when

- The chain is written in true execution order with per-route and global steps distinguished
- Skip and fallthrough points are marked, and any deviation from documentation is recorded

## References

- [OWASP - Authorization validation guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-862 - Missing authorization](https://cwe.mitre.org/data/definitions/862.html)
