---
name: observability-and-ownership-record
description: "Establish who owns the logs and what you are allowed to read in them, because a finding that cannot be traced to its own trace line will not survive review. Use when the assessment will correlate API requests with server-side logs or traces"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [scope, observability, logs]
---

# Observability and Ownership Record

> Establish who owns the logs and what you are allowed to read in them, because a finding that cannot be traced to its own trace line will not survive review

**Use when:** the assessment will correlate API requests with server-side logs or traces

**Avoid when:** the owner supplies read access to the relevant logs with a stated retention and scope

## Procedure

1. Confirm what log and trace access the boundary permits, including which environments and which time window.
2. Identify the correlation identifier the API returns or records, since that is what joins your request to server-side state.
3. Record who owns each log source, so a question during review has a person to reach.
4. Note retention, because a finding traced to a log older than retention cannot be re-checked.
5. Confirm that reading logs will not expose other users' records beyond what the boundary allows.
6. Write the access, correlation method and ownership into the boundary document before the first request.

## Signals

- The boundary says nothing about reading server-side logs
- No correlation identifier joins a request to its server-side trace
- Log retention is shorter than the assessment window
- No one can say who owns the error log for the endpoint under test

## Patterns

**1. Access record**

```text
source: application logs | window: staging, assessment dates | correlation: x-request-id header | owner: platform | retention: 14 days
```

**2. Correlation rule**

```text
every evidence entry records the correlation id, so a reviewer can find the matching server-side line without re-issuing the request
```

**3. Ownership column**

```text
each log source has an owner named; a source with no owner is escalated before it is relied upon
```

## Pitfalls

- Trusting a client-side response as proof of server-side behaviour without a correlated log line
- Reading logs beyond the permitted window or environment
- Relying on a log source whose retention ends before review happens

## Done when

- Log access, correlation method, owners and retention are recorded in the boundary
- Every later evidence entry carries the correlation id that ties it to server-side state

## References

- [OWASP - Logging cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [CWE-778 - Insufficient logging](https://cwe.mitre.org/data/definitions/778.html)
