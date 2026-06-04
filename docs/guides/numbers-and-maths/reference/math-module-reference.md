---
title: math module reference
---

# `math` module reference

The everyday `math` functions on one page. All operate on `float` and return `float` unless noted; the integer functions (`isqrt`, `comb`, `perm`, `factorial`, `gcd`, `lcm`) stay exact in `int`.

```python
import math
```

## Powers, roots, and logarithms

| Function | Returns | Example |
| --- | --- | --- |
| `sqrt(x)` | square root (float) | `sqrt(16)` → `4.0` |
| `isqrt(n)` | integer square root, floored | `isqrt(17)` → `4` |
| `cbrt(x)` | cube root (3.11+) | `cbrt(27)` → `3.0` |
| `pow(x, y)` | `x ** y` as float | `pow(2, 10)` → `1024.0` |
| `exp(x)` | e<sup>x</sup> | `exp(1)` → `2.718…` |
| `log(x[, base])` | natural log, or log to `base` | `log(8, 2)` → `3.0` |
| `log2(x)` / `log10(x)` | log base 2 / base 10 | `log10(1000)` → `3.0` |
| `hypot(*coords)` | Euclidean norm √(Σx²) | `hypot(3, 4)` → `5.0` |

Use the built-in `**`/`pow` for integer powers (exact, any size); use `math.pow` only when you want a float result.

## Rounding (return `int`)

| Function | Rounds | Example |
| --- | --- | --- |
| `floor(x)` | toward −∞ | `floor(-3.2)` → `-4` |
| `ceil(x)` | toward +∞ | `ceil(3.2)` → `4` |
| `trunc(x)` | toward zero | `trunc(-3.7)` → `-3` |

The built-in `round` is separate — it rounds half to *even* and returns the same type. See [round numbers correctly](../recipes/round-numbers-correctly.ipynb).

## Combinatorics and integer maths (return `int`)

| Function | Returns | Example |
| --- | --- | --- |
| `factorial(n)` | n! | `factorial(5)` → `120` |
| `comb(n, k)` | combinations, n choose k | `comb(5, 2)` → `10` |
| `perm(n, k)` | permutations | `perm(5, 2)` → `20` |
| `gcd(*ints)` | greatest common divisor | `gcd(12, 18)` → `6` |
| `lcm(*ints)` | lowest common multiple (3.9+) | `lcm(4, 6)` → `12` |
| `prod(iterable, start=1)` | product of items | `prod([1,2,3,4])` → `24` |

## Trigonometry

Angles are in **radians**. Convert with `degrees`/`radians`.

| Function | Notes |
| --- | --- |
| `sin(x)`, `cos(x)`, `tan(x)` | basic trig |
| `asin`, `acos`, `atan`, `atan2(y, x)` | inverses; `atan2` knows the quadrant |
| `degrees(x)` / `radians(x)` | convert between degrees and radians |
| `sinh`, `cosh`, `tanh` | hyperbolic |

## Constants

| Name | Value |
| --- | --- |
| `math.pi` | `3.141592653589793` |
| `math.e` | `2.718281828459045` |
| `math.tau` | `6.283185307179586` (2π) |
| `math.inf` | floating-point infinity |
| `math.nan` | floating-point not-a-number |

## Testing and comparing

| Function | Returns |
| --- | --- |
| `isnan(x)` | `True` if `x` is `nan` (the only reliable test) |
| `isinf(x)` | `True` if `x` is `±inf` |
| `isfinite(x)` | `True` if neither `nan` nor `inf` |
| `isclose(a, b, *, rel_tol=1e-9, abs_tol=0.0)` | safe float equality |
| `copysign(x, y)` | `x` with the sign of `y` |
| `fabs(x)` | absolute value as float |
| `fsum(iterable)` | accurate sum of floats (tracks error) |
| `fmod(x, y)` | C-style remainder (sign of `x`; differs from `%`) |

For arbitrary precision (beyond `float`), do the maths in `Decimal` — it has its own `sqrt`, `ln`, `log10`, and `exp` methods.
