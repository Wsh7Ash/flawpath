---
name: handler-and-route-inventory
description: "Enumerate every route and its handler, including internal and versioned ones, because an unlisted handler is where a check you assumed exists turns out not to. Use when a backend is in scope and no maintained list of routes with their handlers exists"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, inventory, routes]
---

# Handler and Route Inventory

> Enumerate every route and its handler, including internal and versioned ones, because an unlisted handler is where a check you assumed exists turns out not to

**Use when:** a backend is in scope and no maintained list of routes with their handlers exists

**Avoid when:** framework-generated documentation lists every route with handler and middleware already confirmed current

## Procedure

1. Extract routes from the framework registry or router table rather than from prose documentation that may be stale.
2. Record for each route its method, handler function, middleware chain and the roles permitted to reach it.
3. Flag routes that exist but are undocumented, since these are usually the ones with the oldest checks.
4. Note versioned duplicates where one version kept a check the newer one dropped.
5. Separate public, authenticated and internal-only routes into three lists so coverage is visible per class.
6. Carry undocumented and internal routes into the map phase as explicit questions rather than dropping them.

## Signals

- The router table contains paths absent from the published documentation
- Two API versions expose the same operation with different middleware
- An internal-only route shares a prefix with public routes
- A handler is registered dynamically, so a static route list misses it

## Patterns

**1. Inventory row**

```text
path | method | handler | middleware | roles | documented
/api/v1/orders | GET | list_orders | auth, rate | member | yes
/internal/reindex | POST | reindex | none | internal | no
```

**2. Class split**

```text
public | authenticated | internal; each list is reviewed separately so an internal route with no middleware is visible rather than averaged away
```

**3. Dynamic-route note**

```text
when a route is registered at runtime, record where registration happens so the inventory can be regenerated from that source
```

## Pitfalls

- Building the inventory from documentation, which is exactly what has drifted
- Skipping versioned duplicates, where a dropped check is most likely to be found
- Assuming internal routes are unreachable because a gateway usually fronts them

## Done when

- Every route has a row with method, handler, middleware, permitted roles and documentation status
- Undocumented and internal routes are listed as explicit questions for the map phase

## References

- [OWASP - API documentation and discovery](https://owasp.org/API-Security/)
- [CWE-778 - Insufficient logging](https://cwe.mitre.org/data/definitions/778.html)
