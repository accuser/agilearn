---
title: Choosing a numeric type
---

# Choosing a numeric type

Python gives you four numeric types worth choosing between — `int`, `float`, `Decimal`, and `Fraction` — and most numeric bugs are really a type-choice bug in disguise. Money stored in a `float`, a ratio forced through decimals, an exact count drifting because it went through floating point: each is the wrong type quietly doing its best. This essay is a short framework for picking the right one the first time.

## The question that decides it: must this be exact?

Numbers in programs fall into two camps. Some are **counted or specified exactly** — a number of items, a price, a ratio. Others are **measured or continuous** — a temperature, a coordinate, a probability, a duration. The first camp needs exactness; the second is approximate by its very nature, because the measurement was approximate to begin with.

This single distinction does most of the work:

- **Exact, whole numbers** → `int`. It's exact and unbounded, so counts, indices, identifiers, and integer maths never lose precision or overflow.
- **Exact decimal amounts** → `Decimal`. Money and anything denominated in decimal units with defined rounding.
- **Exact ratios** → `Fraction`. Quantities that are fundamentally fractions and must stay exact.
- **Measured or continuous** → `float`. Everything else — and it's the majority.

## `int`: the default for whole things

If a quantity is conceptually a whole number, keep it one. Python's `int` is exact and has no size limit, so it never surprises you. The only trap is `/`, which always yields a `float`; use `//` when you want to stay in integers. Counting, indexing, money-in-pence (some systems store currency as integer minor units precisely to stay exact), bit manipulation — all `int`.

## `float`: the default for measured things

`float` is fast, compact, hardware-accelerated, and accurate to about 16 significant digits over an enormous range. For anything that came from a sensor, a calculation in physics or statistics, a screen coordinate, or a percentage, that precision dwarfs the uncertainty already in the data, so the representation error (see [how floating point works](how-floats-work.md)) is irrelevant. The cost of `float` is that it's *not exact* — so the moment a value must be exact, it's the wrong choice. Don't reach for `Decimal` out of vague nervousness, though: for genuinely measured quantities, `float` is not a compromise, it's correct.

## `Decimal`: when the decimal digits are the point

Use `Decimal` when a number is *defined* in decimal and the exact digits matter: money, tax, invoices, anything with a published rounding rule. `Decimal` thinks in base 10, so `0.1` is exactly one tenth and a total of pennies stays a total of pennies. It also gives you explicit control over precision and rounding mode, which financial rules often mandate. The price is speed and a little ceremony (build from strings, `quantize` at the end), but when correctness is measured in pennies that ceremony is the job. See [handle money with Decimal](../recipes/handle-money-with-decimal.ipynb).

## `Fraction`: when ratios must stay exact

`Fraction` is the niche but unbeatable choice when your quantities are genuinely rational and thirds, sevenths, or other non-terminating fractions must remain exact through a chain of arithmetic — exact probabilities, gear ratios, slopes, or teaching maths. It keeps a numerator and denominator, auto-reduced, so `⅓ + ⅓ + ⅓` is exactly `1`, which neither `float` nor `Decimal` can promise. You convert to `float` for display or further approximate work at the end.

## A decision table

| The quantity is… | Type | Because |
| --- | --- | --- |
| a count, index, or id | `int` | exact and unbounded |
| money / a decimal amount | `Decimal` | exact in base 10, controllable rounding |
| an exact ratio (thirds, etc.) | `Fraction` | keeps rationals exact |
| measured, continuous, scientific | `float` | fast, ample precision, error irrelevant |
| a truth value used as 0/1 | `bool` | it *is* an `int` |

## The cost of choosing exactness

Exact types aren't free. `Decimal` and `Fraction` are considerably slower than `float` and use more memory, and `Fraction`'s denominators can grow large over long calculations. So the rule isn't "exact is always better" — it's *match the type to the quantity*. Using `Decimal` for a temperature is as much a mismatch as using `float` for a bank balance; one wastes performance, the other risks correctness.

In practice the choice is quick. Ask whether the number must be exact. If it's a whole thing, `int`; if it's decimal money, `Decimal`; if it's a ratio that must stay exact, `Fraction`; and if it's measured, `float` without apology. Get that right at the point you *store* the value, and the arithmetic downstream takes care of itself.
