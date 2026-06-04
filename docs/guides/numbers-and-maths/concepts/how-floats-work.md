---
title: How floating point works
---

# How floating point works

Every few days, somewhere, a programmer discovers that `0.1 + 0.2` is `0.30000000000000004` and files a bug. It isn't a bug, and it isn't Python's — it's how binary floating point works in essentially every language, on essentially every machine. This essay explains *why*, because once the mechanism is clear, the practical rules — don't compare floats with `==`, use `Decimal` for money — stop being arbitrary and start being obvious.

## Scientific notation, in binary

You already know one way to write a number compactly: scientific notation. `6.022 × 10²³` has three parts — a **sign**, a string of **significant digits** (the mantissa, `6.022`), and an **exponent** (`23`) that says where the decimal point goes. You get a fixed number of significant digits and a wide range of magnitudes.

A `float` is exactly this, with one change: the base is **2**, not 10. A number is stored as

> sign × mantissa × 2<sup>exponent</sup>

where the mantissa is a binary fraction. Python's `float` is the IEEE 754 *double*: 64 bits, split into 1 sign bit, 11 exponent bits, and 52 bits of mantissa (which behave as 53 because the leading bit is implied). That's a fixed budget — about 15 to 17 significant *decimal* digits — and a range out to roughly 1.8 × 10³⁰⁸.

## Why `0.1` can't be stored

Here's the crux. In base 10, you can write some fractions exactly with a finite number of digits (½ = 0.5) and others you can't (⅓ = 0.3333…, forever). *Which* fractions terminate depends on the base: a fraction terminates only if its denominator's prime factors are all factors of the base.

Base 10's factors are 2 and 5, so tenths, fifths, and halves all terminate. Base 2's only factor is 2, so in binary **only fractions whose denominator is a power of two terminate** — halves, quarters, eighths. One tenth is not one of them. In binary, `0.1` is the repeating fraction `0.0001100110011…`, exactly as `⅓` repeats in decimal.

Since the mantissa has only 53 bits, the repeating expansion gets cut off and rounded to the nearest value that *does* fit. That stored value isn't `0.1` — it's `0.1000000000000000055511151231257827…`. The error is tiny (about 1 part in 10¹⁶), but it's real, and it's there before you do any arithmetic at all.

## Why the error becomes visible

If `0.1` is slightly wrong and `0.2` is slightly wrong, their sum is slightly-more wrong — and `0.1 + 0.2` lands on a stored value just different enough from the stored `0.3` that the two are distinguishable. `==` compares the full stored values, sees the difference in the last bit, and returns `False`.

So why does plain `print(0.1)` show a tidy `0.1`? Because Python prints the *shortest* decimal string that round-trips back to the same stored float, and for a single `0.1` that's `"0.1"`. The error is still in there; printing just rounds it away. Adding two of these values nudges the result onto a float whose shortest round-tripping string is the ugly `0.30000000000000004`, and the curtain lifts.

## What this means for your code

Three consequences follow directly, and they're the whole practical lesson:

**Don't test floats with `==`.** Two computations that should give the same real number can land on adjacent floats. Ask whether they're close instead — `math.isclose(a, b)` — with an absolute tolerance when comparing against zero.

**Don't use `float` for money.** Currency is defined in exact decimal units — pennies, cents — and "off by one part in 10¹⁶" eventually becomes "off by a penny" once you round for display. Money wants a base-10 type, `Decimal`, where `0.1` really is one tenth.

**Do use `float` for nearly everything else.** Measurements, coordinates, physics, statistics, graphics — anything continuous and already approximate — are perfectly served by a type with 15-plus significant digits. The representation error is far smaller than the measurement error in the data, so it simply doesn't matter.

## The error is bounded, which is what makes floats usable

It's worth ending on the reassuring half of the story. Floating-point error isn't chaos — it's bounded and well understood. Each operation introduces at most half a unit in the last place, and the IEEE 754 standard specifies the behaviour precisely enough that numerical software can reason about and control how error accumulates. Floats are not "imprecise" so much as *finite*: they trade exactness for a vast range and constant-time arithmetic, and for the overwhelming majority of computing that is exactly the right trade. You only need to step outside `float` when a number must be exact — and now you know precisely when that is. The [choosing a numeric type](choosing-a-numeric-type.md) essay turns it into a decision.
