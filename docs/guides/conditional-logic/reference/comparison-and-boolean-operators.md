---
title: Comparison and boolean operators
---

# Comparison and boolean operators

A quick-lookup reference for the operators you use inside conditions. Pairs with the [Learn](../learn/) tutorials if you want the walkthrough.

## Comparison operators

These operators compare two values and return a `bool`.

| Operator | Meaning                  | Example            | Returns  |
|----------|--------------------------|--------------------|----------|
| `==`     | Equal to                 | `3 == 3`           | `True`   |
| `!=`     | Not equal to             | `3 != 4`           | `True`   |
| `<`      | Less than                | `3 < 4`            | `True`   |
| `<=`     | Less than or equal to    | `3 <= 3`           | `True`   |
| `>`      | Greater than             | `4 > 3`            | `True`   |
| `>=`     | Greater than or equal to | `3 >= 3`           | `True`   |
| `is`     | Same object (identity)   | `x is None`        | `True` if `x` *is* the `None` singleton |
| `is not` | Not the same object      | `x is not None`    | negation of `is` |
| `in`     | Membership               | `3 in [1, 2, 3]`   | `True`   |
| `not in` | Non-membership           | `"q" not in "abc"` | `True`   |

### Equality versus identity

`==` asks "are these values equal?" `is` asks "are these two names bound to the exact same object in memory?"

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True  — same contents
a is b  # False — two separate list objects
```

Use `is` only for singletons: `None`, `True`, `False`. For everything else, prefer `==`.

### Chained comparisons

Python lets you chain comparisons, and it reads them the way maths does:

```python
0 < x < 10          # equivalent to (0 < x) and (x < 10)
a == b == c         # equivalent to (a == b) and (b == c)
```

The middle term is evaluated once. This is more efficient and more readable than the explicit `and` form.

## Boolean operators

| Operator | Meaning            | Short-circuits on |
|----------|--------------------|-------------------|
| `and`    | Both must be truthy | first falsy value |
| `or`     | At least one truthy | first truthy value |
| `not`    | Logical negation    | n/a               |

### Short-circuit evaluation

`and` and `or` stop evaluating as soon as the answer is known:

```python
x and y     # if x is falsy, y is never evaluated
x or y      # if x is truthy, y is never evaluated
```

This lets you use them as guards:

```python
name = get_user() and get_user().name  # safe if get_user() returns None
items = raw_items or []                # default if raw_items is None/empty
```

### `and`/`or` return one of their operands

This often surprises people: `and` and `or` do **not** return `True` or `False`. They return whichever operand decided the outcome:

```python
"" or "default"       # "default"
"hello" or "default"  # "hello"
0 and 1               # 0
1 and 2               # 2
```

That's what makes the `items = raw_items or []` idiom work.

## Operator precedence

From loosest to tightest binding, the operators relevant to conditionals:

1. `or`
2. `and`
3. `not`
4. `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==`
5. Arithmetic and everything else

So `not x == y` parses as `not (x == y)`, not `(not x) == y`. When in doubt, parenthesise.

## Related pages

- [Truthiness rules](truthiness-rules.md) — what counts as truthy or falsy
- [`match`/`case` syntax](match-case-syntax.md) — the structural alternative to long `if`/`elif` chains
