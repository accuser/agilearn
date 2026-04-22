# Avoid common conditional mistakes

**The question.** You're reviewing a conditional and something feels off — a comparison uses `is` where `==` belongs, a truthiness check quietly treats `0` as missing, or an `else` is hanging after a `return`. You want a quick way to recognise the common traps and know what each should look like instead.

The pattern is almost always *"this shortcut works 90% of the time — here's the 10% where it bites."* Below is the summary, then each mistake in detail.

## The answer

| Looks like… | Means… | Use instead |
| --- | --- | --- |
| `if x is 0:` | Object-identity check (only works by accident) | `if x == 0:` |
| `if x == True:` | Verbose, breaks for non-booleans | `if x:` |
| `if items:` to mean "not None" | Also false for `[]`, `0`, `''` | `if items is not None:` |
| `0.1 + 0.2 == 0.3` | `False` (floating-point) | `math.isclose(a, b)` |
| `if a < b < c:` | `(a < b) and (b < c)`, chained | `if (a < b) == (c < d):` if that's what you meant |
| `else:` after `return` | Redundant scaffolding | Drop the `else`, let the next line return |
| `def f(x, seen=[]):` | Shared mutable default | `def f(x, seen=None):` + `if seen is None: seen = []` |
| `if not a or b:` | `(not a) or b` | `if not (a or b):` if you meant "neither" |

The rest of this recipe goes trap by trap.

## `==` versus `is`

`==` compares values. `is` compares identity (same object in memory).

```python
# WRONG — happens to work for small ints because of interning, but for the wrong reason
if count is 0:
    ...

# RIGHT
if count == 0:
    ...
```

**Rule of thumb:** use `is` only with singletons — `None`, `True`, and `False`. For everything else, use `==`. `x is None` is both idiomatic and correct.

## The `if x == True` antipattern

If `x` is already a boolean, `if x == True:` is `if True == True:` — redundant. If `x` isn't a boolean, the comparison does something different from what you probably meant.

```python
# Noisy
if is_valid == True:
    ...

# Right
if is_valid:
    ...
```

Same for `== False` — write `if not is_valid:`.

## `if x:` when you mean `if x is not None:`

These two look similar but mean different things. `if items:` is `False` for `None`, `[]`, `''`, `0` — any falsy value. `if items is not None:` is only `False` for `None`. When `0`, `""`, or `[]` are meaningful values, the difference matters. The classic bug:

```python
def save(name, count=None):
    if count:                 # bug — treats count=0 as "missing"
        record(name, count)

def save(name, count=None):
    if count is not None:     # correct — 0 is a real count
        record(name, count)
```

## Comparing floats with `==`

Floating-point arithmetic isn't exact. `0.1 + 0.2 == 0.3` is `False`. Use `math.isclose` for approximate equality, and `decimal.Decimal` for financial calculations where exactness matters.

```python
import math
math.isclose(0.1 + 0.2, 0.3)            # True
math.isclose(a, b, rel_tol=1e-9)         # tighten as needed
```

## The chained-comparison surprise

Chained comparisons are a feature, not a bug — but they can surprise you when you misread the chain:

```python
a, b, c = 5, 10, 3

if a < b < c:     # This is (a < b) and (b < c) — NOT (a < b) < c
    ...            # 5 < 10 and 10 < 3 → False
```

That's the intended behaviour — it matches maths notation. The trap is assuming the chain reduces left-to-right like arithmetic does. When each comparison should stand on its own, write them out explicitly.

## Redundant `else` after `return`

Once a branch has returned, the `else` is scaffolding with no load:

```python
# Verbose
def classify(n):
    if n > 0:
        return 'positive'
    else:
        if n == 0:
            return 'zero'
        else:
            return 'negative'

# Cleaner
def classify(n):
    if n > 0:
        return 'positive'
    if n == 0:
        return 'zero'
    return 'negative'
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

## When the shortcut is fine

Every one of these is a *pattern*, not an absolute rule. `if items:` is the right check when you explicitly want "non-empty, non-None, non-zero" — and that's often what you want. `==` on floats is fine for integer-valued floats (`3.0 == 3` is `True`). Chained comparisons are the clearest way to say `0 <= i < len(xs)`.

The traps bite when the shortcut is applied out of habit to a case where the defaults don't match the intent. The fix isn't to ban the shortcut — it's to notice when you need to spell the condition out.

## Related reading

- [Comparison and boolean operators](../reference/comparison-and-boolean-operators.md) — the operator semantics in one place.
- [Truthiness rules](../reference/truthiness-rules.md) — the canonical list of falsy values.
- [Use guard clauses to flatten nested conditions](use-guard-clauses.ipynb) — the refactoring that removes most redundant-`else` cases.
