---
title: Numbers and maths
---

# Numbers and maths

Numbers look like the simplest thing in any language, and most of the time they are — until `0.1 + 0.2` doesn't equal `0.3`, a total comes out a penny short, or a rounding rule surprises you. Python actually gives you several different number types, each making a different trade between speed, range, and exactness, and most number bugs come from using the wrong one for the job.

This guide covers the lot: the built-in `int`, `float`, and `complex`; the exact `Decimal` and `Fraction` types for money and ratios; and the `math`, `statistics`, and `random` modules from the standard library. The recurring theme is a single question — *do I need this to be exact?* — and matching the answer to the right type.

## Sections

- **[Learn](learn/)** — four notebooks: the numeric types and their arithmetic, how floating point really behaves (and why), exact arithmetic with `Decimal` and `Fraction`, and a tour of `math`, `statistics`, and `random`.
- **[Recipes](recipes/)** — rounding numbers correctly, handling money with `Decimal`, formatting numbers for display, and the mistakes that cost a penny or a debugging hour.
- **[Reference](reference/)** — a `math` module reference, the number side of the format mini-language, and a numeric-types-and-operators lookup.
- **[Concepts](concepts/)** — essays on how floating point works under the hood, and on choosing the right numeric type for a given job.

New to the topic? Start with [Learn → Numeric types](learn/01-numeric-types.ipynb). Here for a specific task? [Recipes](recipes/) is task-focused and [Reference](reference/) is for lookups.
