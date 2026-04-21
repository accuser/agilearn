---
title: Avoid common conditional mistakes
---

# Avoid common conditional mistakes

A round-up of the traps that catch people when writing conditionals — not because the language is hostile, but because the shortcuts are real shortcuts and the sharp corners are easy to miss.

## `==` versus `is`

`==` compares values. `is` compares object identity (same object in memory).

```python
# WRONG — happens to work for small ints because of interning, but for the wrong reason
if count is 0:
    ...

# RIGHT
if count == 0:
    ...
```

**Rule of thumb:** use `is` only with singletons — `None`, `True`, and `False`. For everything else, use `==`. `None` is a singleton, so `x is None` is both idiomatic and correct.

```python
if user is None:
    user = create_guest()
```

## The `if x == True` antipattern

If `x` is already a boolean, `if x == True:` is `if True == True:` — redundant and louder than it needs to be. If `x` *isn't* a boolean, the comparison does something different from what you probably meant.

```python
# Noisy
if is_valid == True:
    ...

# Right
if is_valid:
    ...
```

Same for `== False`:

```python
# Noisy
if is_valid == False:
    ...

# Right
if not is_valid:
    ...
```

## `if x:` when you mean `if x is not None:`

These two look similar but mean different things:

```python
if items:
    # True when items is a non-empty sequence
    # False when items is None, empty list, empty string, 0, ...

if items is not None:
    # True when items is anything other than None
    # including empty lists, zero, empty strings
```

When you pass `0`, `""`, or `[]` around as meaningful values, the difference matters. The classic bug:

```python
def save(name, count=None):
    if count:                 # bug — treats count=0 as "missing"
        record(name, count)

def save(name, count=None):
    if count is not None:     # correct — 0 is a real count
        record(name, count)
```

## Comparing floats with `==`

Floating-point arithmetic isn't exact, and equality checks will disappoint you:

```python
0.1 + 0.2 == 0.3    # False
```

Use `math.isclose` for approximate equality:

```python
import math

math.isclose(0.1 + 0.2, 0.3)    # True
math.isclose(a, b, rel_tol=1e-9)
```

For financial calculations, reach for `decimal.Decimal` and compare exactly.

## The chained comparison surprise

Chained comparisons are a feature, not a bug — but they can surprise you when you misread the chain:

```python
a = 5
b = 10
c = 3

if a < b < c:     # This is (a < b) and (b < c) — NOT (a < b) < c
    ...           # Evaluates to (5 < 10) and (10 < 3) — False
```

That's the intended behaviour (and it's what maths notation does). The trap is assuming the chain reduces left-to-right like arithmetic does. When each comparison should stand on its own, write them out:

```python
if (a < b) == (c < d):
    ...
```

## Redundant `else` after `return`

Once a branch has returned, the `else` is scaffolding with no load:

```python
# Verbose
def classify(n):
    if n > 0:
        return "positive"
    else:
        if n == 0:
            return "zero"
        else:
            return "negative"

# Cleaner
def classify(n):
    if n > 0:
        return "positive"
    if n == 0:
        return "zero"
    return "negative"
```

This is a special case of the [guard clauses pattern](use-guard-clauses.ipynb) — the early return *is* the guard.

## Mutable defaults in conditional branches

Not strictly a conditional mistake, but it bites often enough to warrant a mention — and conditionals are where it's most likely to sneak past review:

```python
# WRONG — the default [] is shared across calls
def append_if_new(item, seen=[]):
    if item not in seen:
        seen.append(item)
    return seen

# RIGHT
def append_if_new(item, seen=None):
    if seen is None:
        seen = []
    if item not in seen:
        seen.append(item)
    return seen
```

## The `if not a or b` precedence trap

`not` binds tighter than `and` and `or`:

```python
if not a or b:      # means (not a) or b
if not (a or b):    # means "neither a nor b"
```

These are different. Parenthesise whenever there's any doubt — your future self will thank you.

## Related reading

- [Comparison and boolean operators](../reference/comparison-and-boolean-operators.md) — the operator semantics in one place.
- [Truthiness rules](../reference/truthiness-rules.md) — the canonical list of falsy values.
- [Use guard clauses to flatten nested conditions](use-guard-clauses.ipynb) — the refactoring that removes most redundant-`else` cases.
