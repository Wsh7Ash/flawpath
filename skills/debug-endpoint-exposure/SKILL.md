---
name: debug-endpoint-exposure
description: "Look for framework debug, health and introspection routes reachable without the authentication the rest of the API requires. Use when the route inventory includes debug, metrics, health or introspection paths"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, debug, routes]
---

# Debug Endpoint Exposure

> Look for framework debug, health and introspection routes reachable without the authentication the rest of the API requires

**Use when:** the route inventory includes debug, metrics, health or introspection paths

**Avoid when:** those routes are all behind authentication and a test confirms a rejection for each

## Procedure

1. List every debug, metrics, health, and introspection path from the route inventory.
2. Request each without credentials and record status, body and timing against the baseline.
3. For any that answer, record which fields the body exposes: configuration, routes, versions or environment.
4. Check whether the environment delta explains the exposure, since debug routes often follow a debug flag.
5. Note whether these paths are excluded from logging while others are logged.
6. Record each path with reachable, rejected or absent as its verdict, plus what a reachable one disclosed.

## Signals

- A debug or introspection route answers without authentication
- A metrics endpoint reveals internal names, counts or versions
- An unauthenticated route returns configuration detail absent from normal responses
- A debug path is excluded from the access log

## Patterns

**1. Route verdict**

```text
path | auth required | status | discloses | in log
/debug/routes | no | 200 | full route table | no
/metrics | no | 200 | version and counts | yes
/health | no | 200 | nothing sensitive | yes
```

**2. Environment link**

```text
tie each exposure back to the environment delta, since a debug route enabled by a flag is a configuration finding
```

**3. Logging note**

```text
record whether the path is logged; an unlogged debug route is a second finding on the same path
```

## Pitfalls

- Reporting a health endpoint as exposed without saying what it actually disclosed
- Missing that a debug route is gated by an environment flag rather than by authentication
- Ignoring that the route may be excluded from logs, which changes the response

## Done when

- Every debug and introspection path has a verdict with what it disclosed if reachable
- Each exposure is linked to the environment delta and its logging status

## References

- [OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- [CWE-489 - Active debug code](https://cwe.mitre.org/data/definitions/489.html)
