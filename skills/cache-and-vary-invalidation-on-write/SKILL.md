---
name: cache-and-vary-invalidation-on-write
description: "Check whether a write invalidates the cached reads it should, because a stale read after a mutation is a correctness defect that only appears when you look. Use when responses can be cached and writes update the same data the cache serves"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, caching, state]
---

# Cache and Vary Invalidation on Write

> Check whether a write invalidates the cached reads it should, because a stale read after a mutation is a correctness defect that only appears when you look

**Use when:** responses can be cached and writes update the same data the cache serves

**Avoid when:** the owner confirms no caching layer exists between client and origin for these paths

## Procedure

1. Capture a read of a synthetic record and note any caching headers in the response.
2. Perform a permitted write to that record and record the write response.
3. Repeat the read immediately and compare the returned state against the write you just made.
4. Record whether the read came from cache, using the status headers, and how stale it was.
5. Check whether the vary dimensions would let another client receive the stale copy.
6. Record the invalidation behaviour as immediate, delayed with a measured window, or absent.

## Signals

- A read after a write returns the pre-write state
- The stale read carries a cache status showing it was served from storage
- No vary dimension separates clients, so the stale copy can reach another caller
- Invalidation happens only after a delay long enough to observe

## Patterns

**1. Sequence record**

```text
read -> cached | write -> 200 | read again -> stale, status hit, age 12s; verdict: invalidation absent
```

**2. Window measure**

```text
when invalidation is delayed, record the observed window so the report gives a number rather than a word
```

**3. Vary note**

```text
state whether vary dimensions would isolate clients, since that decides whether staleness stays yours or spreads
```

## Pitfalls

- Reporting staleness without confirming the second read was actually cached
- Attributing staleness to the application when a downstream layer holds the copy
- Ignoring that your own client may have cached, which is not the server's defect

## Done when

- A read-write-read sequence has all three recorded states with cache status
- Invalidation is labelled immediate, delayed with a window, or absent

## References

- [IETF RFC 9111 - HTTP caching](https://www.rfc-editor.org/rfc/rfc9111)
- [OWASP - Cache-related testing](https://owasp.org/www-project-web-security-testing-guide/)
