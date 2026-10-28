---
name: debug-surface-disabled-in-shared-environments
description: "Turn off debug, introspection and verbose error paths in any environment more than one person can reach, and verify by request rather than by configuration reading. Use when a debug or introspection route is reachable or verbose errors are enabled outside a local environment"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [harden, debug, configuration]
---

# Debug Surface Disabled in Shared Environments

> Turn off debug, introspection and verbose error paths in any environment more than one person can reach, and verify by request rather than by configuration reading

**Use when:** a debug or introspection route is reachable or verbose errors are enabled outside a local environment

**Avoid when:** every debug surface is disabled in shared environments and a request confirms it

## Procedure

1. List every debug, introspection, metrics-detail and verbose-error surface found during probing.
2. Disable each in shared environments, or place it behind authentication if it must remain available.
3. Prefer removing the route over flagging it, since a flag can be flipped back by a later deploy.
4. Verify by issuing the same requests that found the exposure and confirming rejection or absence.
5. Confirm the environment delta now records the setting as disabled in every shared environment.
6. Re-run the debug-endpoint probe and record the result beside the change.

## Signals

- A debug route is gated by a flag that a later deploy could re-enable
- The fix is a configuration change with no verification request recorded
- One shared environment still answers a debug path after others were closed
- The environment delta still lists the debug setting as enabled

## Patterns

**1. Closure record**

```text
surface | action | verification request | result
/debug/routes | removed | GET -> 404 | confirmed absent
verbose errors | flag off | trigger -> uniform body | confirmed
```

**2. Remove-over-flag**

```text
removal survives a deploy; a flag flipped by a later change does not, so prefer deletion where the route has no legitimate use
```

**3. Delta update**

```text
the environment delta row is updated in the same change, so the record and the reality stay aligned
```

## Pitfalls

- Closing a debug route in one environment while another shared environment keeps it
- Recording a configuration edit as the fix without a request proving the surface is gone
- Leaving the setting enabled in the delta, which makes the next assessment repeat the work

## Done when

- Each debug surface has an action and a verification request with a recorded result
- The environment delta reflects the disabled state in every shared environment

## References

- [CWE-489 - Active debug code](https://cwe.mitre.org/data/definitions/489.html)
- [OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
