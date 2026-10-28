---
name: type-coercion-in-write-path
description: "Check whether a value of the wrong type is coerced rather than rejected, because a coerced boolean or number changes what a later authorization check actually tests. Use when the write path accepts values whose types have not been exercised against the parser's coercion rules"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, coercion, validation]
---

# Type Coercion in Write Path

> Check whether a value of the wrong type is coerced rather than rejected, because a coerced boolean or number changes what a later authorization check actually tests

**Use when:** the write path accepts values whose types have not been exercised against the parser's coercion rules

**Avoid when:** the schema is strict about types and a test confirms an out-of-range type is rejected

## Procedure

1. List the typed fields on the write path: booleans, numbers, enumerations and identifiers.
2. For each, send one value of a different type on a synthetic record you own and read the object back.
3. Record whether the value was rejected, stored as sent, or coerced into the declared type.
4. For coercions, record the rule observed: string to number, truthy string to boolean, array to single value.
5. Check whether the coerced value would change a downstream decision such as a feature check.
6. Record a coercion table with one row per field and its observed behaviour.

## Signals

- A string such as a word is accepted for a boolean field and stored truthy
- A numeric field accepts a string and stores it without conversion
- An array is accepted where a scalar is declared and later truncated
- A coerced value changes a feature or authorization decision downstream

## Patterns

**1. Coercion table**

```text
field | type declared | value sent | result
active | boolean | "no" | stored true  <- truthy coercion
quantity | integer | "12" | stored 12
role | enum | ["admin"] | stored admin
```

**2. Downstream check**

```text
after a coercion, record whether the coerced value reaches a decision; a stored-but-unused field is far lower impact
```

**3. Rule naming**

```text
write the observed coercion rule in words, since the report needs the rule rather than a single example
```

## Pitfalls

- Recording a coercion without checking whether anything downstream consumes the value
- Testing one type per class and missing the specific type that changes a decision
- Attributing a rejection to validation when the parser rejected it earlier in the chain

## Done when

- A coercion table records declared type, value sent and result for each typed field
- At least one coercion is traced to its downstream decision, or recorded as unused

## References

- [CWE-704 - Incorrect type conversion](https://cwe.mitre.org/data/definitions/704.html)
- [OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
