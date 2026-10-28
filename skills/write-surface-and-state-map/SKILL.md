---
name: write-surface-and-state-map
description: "Establish which objects are writable and which transitions each write can trigger, because a state change you did not expect is the real effect of a mass-assignment defect. Use when the API mutates domain objects and the reachable transitions have not been enumerated"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, state, inventory]
---

# Write Surface and State Map

> Establish which objects are writable and which transitions each write can trigger, because a state change you did not expect is the real effect of a mass-assignment defect

**Use when:** the API mutates domain objects and the reachable transitions have not been enumerated

**Avoid when:** the API is read-only, or a documented state model covers every writable object

## Procedure

1. List every domain object the API can create, update or delete, with the endpoint that performs each operation.
2. For each object, list the states it can be in and the transitions the endpoints can cause.
3. Mark which transitions are intended for which role, since that is the expectation a defect would break.
4. Note transitions reachable through an update endpoint rather than a dedicated one, which is where unexpected paths appear.
5. Record what rollback or compensation exists for each permitted write, so testing can be undone.
6. Carry the map into the probe phase as the set of intended transitions to compare against observed ones.

## Signals

- An update endpoint can set a field that a dedicated transition endpoint also controls
- No documented state model exists for an object with several visible states
- A transition appears reachable that the role matrix says belongs to another role
- No rollback path exists for a write the boundary permits

## Patterns

**1. Transition row**

```text
object: order | transition: draft -> paid | intended role: billing service | reachable via: PATCH /orders/{id} (status field)
```

**2. Unexpected-path flag**

```text
a transition reachable through a generic update endpoint rather than its dedicated operation is flagged, since that is the usual defect shape
```

**3. Rollback column**

```text
each permitted write carries a rollback: undo endpoint, compensating call, or none; none means the write must be avoided or carefully bounded
```

## Pitfalls

- Testing only the dedicated transition endpoint while the generic update reaches the same state
- Assuming a transition is impossible because no endpoint is documented for it
- Performing a permitted write with no rollback when the boundary required one

## Done when

- Every writable object has a row with intended transitions, roles and rollback status
- Transitions reachable through generic update endpoints are flagged explicitly

## References

- [OWASP - Broken object level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [CWE-284 - Improper access control](https://cwe.mitre.org/data/definitions/284.html)
