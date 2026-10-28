---
name: uniform-error-response-and-correlation
description: "Return one response shape for each error class with a correlation id, so a caller cannot map your internals by trying different malformed inputs. Use when the error surface map shows differing shapes, disclosed field names or stack detail"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [harden, errors, disclosure]
---

# Uniform Error Response and Correlation

> Return one response shape for each error class with a correlation id, so a caller cannot map your internals by trying different malformed inputs

**Use when:** the error surface map shows differing shapes, disclosed field names or stack detail

**Avoid when:** one formatter already handles every error and a probe confirms uniform output

## Procedure

1. Group the mapped errors into classes: validation, authorization, not found, conflict and internal.
2. Give each class one status and one body shape, with no per-condition detail beyond a stable code.
3. Move the specific reason into the server log and put a correlation id in the response.
4. Confirm the formatter runs for every path, including errors raised before the handler and in middleware.
5. Re-run every controlled error trigger and confirm each now returns the uniform shape for its class.
6. Record the before and after shapes so the reduction in disclosed detail is provable.

## Signals

- Different conditions within one class return different messages or codes
- An error raised in middleware returns a framework default rather than the uniform shape
- A response body contains a field name, a query fragment or a stack frame
- The correlation id is absent, leaving operators unable to diagnose a real failure

## Patterns

**1. Class table**

```text
class | status | body | reason location
validation | 400 | {code, correlation_id} | server log
authorization | 403 | {code, correlation_id} | server log
internal | 500 | {code, correlation_id} | server log
```

**2. Coverage check**

```text
test an error raised in middleware and one before the handler runs, since both usually bypass an application-level formatter
```

**3. Retest sweep**

```text
re-run every trigger from the leak table; all must return their class's single shape byte for byte
```

## Pitfalls

- Unifying the body while statuses still differ per condition, which leaks through the code
- Fixing only errors raised inside handlers while middleware keeps returning framework defaults
- Removing the correlation id, which leaves operators unable to diagnose

## Done when

- Every error class has one status and one body shape with a correlation id
- Pre-handler and middleware error paths return the same uniform shape, with the retest sweep recorded

## References

- [CWE-209 - Generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)
- [OWASP - Error handling guidance](https://owasp.org/www-project-web-security-testing-guide/)
