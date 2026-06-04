---
title: Numeric types and operators reference
---

# Numeric types and operators reference

A compact lookup for Python's numeric types, the operators that work on them, and the numeric built-ins.

## The types

| Type | Literal | Exact? | Use for |
| --- | --- | --- | --- |
| `int` | `42`, `0xff`, `1_000` | yes, unbounded | counts, indices, ids, integer maths |
| `float` | `3.14`, `1e6` | no — IEEE 754 double | measurements, science, anything continuous |
| `complex` | `2 + 3j` | no (two floats) | signal processing, maths |
| `Decimal` | `Decimal('1.50')` | yes, base-10 | money, decimal amounts with set rounding |
| `Fraction` | `Fraction(1, 3)` | yes, rational | exact ratios |
| `bool` | `True`, `False` | — (subclass of `int`) | truth values; `True == 1` |

`Decimal` is in the `decimal` module, `Fraction` in `fractions`. Both should be built from **strings**, not floats.

## Arithmetic operators

| Operator | Operation | Note |
| --- | --- | --- |
| `+` `-` `*` | add, subtract, multiply | |
| `/` | true division | **always** returns `float` |
| `//` | floor division | rounds toward −∞; `int` if both operands are `int` |
| `%` | remainder (modulo) | sign matches the divisor |
| `**` | exponentiation | `2 ** 0.5`; exact and unbounded for `int` exponents |
| `-x` `+x` | negation, unary plus | |

`divmod(a, b)` returns `(a // b, a % b)` together. Mixed-type expressions widen to the more general type (`int` + `float` → `float`).

## Bitwise operators (integers)

| Operator | Operation | Example |
| --- | --- | --- |
| `&` | AND | `0b1100 & 0b1010` → `8` |
| `\|` | OR | `0b1100 \| 0b1010` → `14` |
| `^` | XOR | `0b1100 ^ 0b1010` → `6` |
| `~` | NOT (bit inversion) | `~5` → `-6` |
| `<<` | left shift | `1 << 4` → `16` |
| `>>` | right shift | `256 >> 2` → `64` |

## Numeric built-ins

| Function | Returns |
| --- | --- |
| `abs(x)` | absolute value (or magnitude of a `complex`) |
| `round(x[, n])` | round half to even; `n` decimal places, same type back |
| `pow(x, y[, z])` | `x ** y`, or `(x ** y) % z` efficiently |
| `divmod(a, b)` | `(quotient, remainder)` |
| `min(...)` / `max(...)` | smallest / largest |
| `sum(iterable[, start])` | total (pass `Decimal('0')` to keep that type) |
| `int(x[, base])` | convert/parse to `int` (truncates floats toward zero) |
| `float(x)` | convert to `float` |
| `complex(re, im)` | build a complex number |
| `bin(n)` / `oct(n)` / `hex(n)` | base-prefixed string of an `int` |

## Conversion rules

| From → to | Behaviour | Example |
| --- | --- | --- |
| `float` → `int` | truncates toward zero (not rounding) | `int(3.9)` → `3`, `int(-3.9)` → `-3` |
| `str` → `int` | integer strings only; `base` optional | `int('ff', 16)` → `255` |
| `str` → `float` | accepts decimals, `inf`, `nan` | `float('3.5')` → `3.5` |
| `str` → `int` (decimal text) | **raises `ValueError`** | use `int(float('3.5'))` |
| `int`/`str` → `Decimal` | exact | `Decimal('1.50')` |
| `float` → `Decimal` | exact but imports the float's error | avoid; prefer the string |

## Inspecting numbers

| Expression | Returns |
| --- | --- |
| `type(x)` | the exact type |
| `isinstance(x, int)` | type check (note `bool` is an `int`) |
| `n.bit_length()` | bits needed to represent `int` `n` |
| `x.is_integer()` | `True` if a `float` has no fractional part |
| `x.as_integer_ratio()` | `(numerator, denominator)` of a `float`/`Decimal` |
