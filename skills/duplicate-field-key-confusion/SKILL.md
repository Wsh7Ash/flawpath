---
name: duplicate-field-key-confusion
description: "Send the same field twice with different values and see which one wins, because two parsers disagreeing on which value to take is a decision made without anyone deciding. Use when the body can contain a repeated key and precedence has not been observed"
pack: flawpath
version: 1.0.0
category: backend-api
tags: [probe, parsing, confusion]
---

# Duplicate Field Key Confusion

> Send the same field twice with different values and see which one wins, because two parsers disagreeing on which value to take is a decision made without anyone deciding

**Use when:** the body can contain a repeated key and precedence has not been observed

**Avoid when:** a strict parser rejects duplicate keys and a test confirms it

## Procedure

1. Send a permitted update containing one field name twice with two different values on a record you own.
2. Read the object back and record which of the two values was stored.
3. Repeat with the two values swapped to see whether the rule is first-wins, last-wins or something else.
4. If a gateway or proxy sits in front, note whether it may normalize the body before the application sees it.
5. Check whether an authorization decision would depend on which value is taken.
6. Record the precedence rule observed, with both orders tested.

## Signals

- One value wins and the application takes a different one from what a client would assume
- Swapping the order changes which value is stored
- The gateway and the application disagree about which value is present
- An authorization-relevant field is subject to the ambiguity

## Patterns

**1. Precedence record**

```text
field sent twice: {a: 1, a: 2} -> stored 2 (last wins)
reversed: {a: 2, a: 1} -> stored 1; rule: last-wins, confirmed by both orders
```

**2. Layer question**

```text
if a gateway rewrites the body, record whether it preserves duplicates, because the application may never see the pair you sent
```

**3. Decision flag**

```text
mark any precedence ambiguity on a field that reaches an authorization or state decision as the higher-impact case
```

## Pitfalls

- Sending both values in one order and assuming a rule without the reverse test
- Attributing the outcome to the application when a gateway normalized the body first
- Reporting ambiguity on a field nothing consumes while a decision-relevant field goes untested

## Done when

- Both orderings of a duplicate key have a recorded stored value
- The precedence rule is stated, and any decision-relevant field is flagged

## References

- [CWE-436 - Interpretation conflict](https://cwe.mitre.org/data/definitions/436.html)
- [OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
