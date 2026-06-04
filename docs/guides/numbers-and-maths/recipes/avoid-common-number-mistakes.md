# Avoid common number mistakes

**The question.** A calculation is *almost* right — off by a penny, off in the 16th decimal, or returning `False` when two numbers look equal. You want the short list of numeric traps and the fix for each.

Nearly all of them come from one root cause: `float` is an approximation, and treating it as exact. The rest are small surprises in how `round`, `nan`, and the division operators behave.

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `0.1 + 0.2 == 0.3` is `False` | floats are binary approximations | `math.isclose(a, b)` |
| `Decimal(0.1)` is `0.1000…0555` | the float `0.1` is already wrong before `Decimal` sees it | build from a string: `Decimal('0.1')` |
| `round(2.5)` is `2` | `round` rounds half to *even* | `Decimal.quantize(..., ROUND_HALF_UP)` |
| `Decimal('1.5') + 0.1` raises `TypeError` | mixing exact and approximate is blocked | keep the whole calculation in `Decimal` |
| `nan == nan` is `False` | `nan` is never equal to anything | `math.isnan(x)` |
| `10 / 2` is `5.0`, not `5` | `/` always returns a `float` | use `//` for an integer result |
| `-7 // 2` is `-4`, not `-3` | floor division rounds toward −∞ | expected behaviour — use `int(a / b)` to truncate toward zero |
| `sum([0.1] * 10)` is `0.9999…` | float errors accumulate | `math.fsum(...)`, or sum `Decimal`s |
| `round(2.675, 2)` is `2.67` | `2.675` is stored as `2.6749…` | round a `Decimal('2.675')` instead |
| `a is b` is `False` for `a = b = 500` | only small ints are cached | compare numbers with `==`, never `is` |
| `int('3.5')` raises `ValueError` | `int` won't parse a decimal string | `int(float('3.5'))` |
| a token from `random` is guessable | `random` isn't cryptographically secure | use the `secrets` module |

Each in turn below.

## Why each one bites

### 1. Comparing floats with `==`

Float results carry tiny representation errors, so exact equality is unreliable. Ask whether they're close enough:

```python
import math
math.isclose(0.1 + 0.2, 0.3)          # True
math.isclose(a, b, abs_tol=1e-9)      # give an absolute tolerance near zero
```

### 2. `Decimal` built from a float

`Decimal(0.1)` receives the already-broken float and preserves all of its error. Construct from a string (or int) so the value is exact:

```python
Decimal('0.1')        # exactly one tenth
Decimal(0.1)          # 0.1000000000000000055511151231257827021181583404541015625
```

### 3. `round`'s banker's rounding

`round` sends exact halves to the nearest even digit, so `round(0.5) == 0` and `round(2.5) == 2`. For the "halves go up" rule, round a `Decimal`:

```python
from decimal import Decimal, ROUND_HALF_UP
Decimal('2.5').quantize(Decimal('1'), rounding=ROUND_HALF_UP)   # 3
```

### 4. Mixing `Decimal` and `float`

`Decimal('1.5') + 0.1` raises `TypeError` on purpose — combining an exact value with an approximate one would throw away the exactness. Keep money and other exact work entirely in `Decimal` (mixing with `int` is fine).

### 5. `nan` comparisons

`nan` is, by definition, not equal to anything — including itself — so `==` can't detect it and a `nan` in your data quietly poisons sorts, `min`/`max`, and equality checks:

```python
import math
x = float('nan')
x == x            # False
math.isnan(x)     # True — the only reliable test
```

### 6. `/` versus `//`

True division `/` always produces a `float`, even when the result is whole (`10 / 2` is `5.0`). When you want an integer — an index, a count, a page number — use floor division `//`.

### 7. Floor division rounds toward negative infinity

`//` floors, so `-7 // 2` is `-4`, not `-3`. This is deliberate and makes `%` well-behaved for wrapping, but if you want truncation toward zero, convert a true-division result: `int(-7 / 2)` is `-3`.

### 8. Accumulated float error in `sum`

Adding many floats lets the small errors pile up: `sum([0.1] * 10)` is `0.9999999999999999`. For an accurate float total use `math.fsum`, which tracks the error; for exactness, sum `Decimal`s:

```python
import math
math.fsum([0.1] * 10)     # 1.0
```

### 9. Rounding to decimal places surprises

`round(2.675, 2)` gives `2.67` because `2.675` can't be stored exactly — it's really `2.67499…`. If the exact decimal matters, work from a `Decimal('2.675')`, where the value is what you typed.

### 10. Using `is` to compare numbers

`is` tests object identity, not value. CPython caches small integers (−5 to 256) so `256 is 256` happens to be `True`, but `500 is 500` may be `False`. The interning is an implementation detail — always compare numbers with `==`.

### 11. Parsing strings to numbers

`int('3.5')` raises `ValueError`: `int` parses only integer strings. Convert through `float` first, or use `float` directly:

```python
int(float('3.5'))     # 3
int('10', 2)          # 2  — parse '10' as binary
```

### 12. `random` is not secure

`random` is a fast, reproducible pseudo-random generator — perfect for simulations and tests, predictable for an attacker. For passwords, tokens, API keys, or anything security-sensitive, use `secrets`:

```python
import secrets
secrets.token_hex(16)            # a secure random token
secrets.choice(candidates)       # a secure random pick
```

## The meta-lesson

When a number has to be **exact** — money, anything with a published rounding rule, anything compared for equality — don't use `float`. Use `int` where you can, `Decimal` for decimal amounts, `Fraction` for ratios, and compare with `math.isclose` whenever a `float` is unavoidable. Most numeric bugs disappear the moment the type matches the need; the [choosing a numeric type](../concepts/choosing-a-numeric-type.md) essay is the guide to getting that choice right.
