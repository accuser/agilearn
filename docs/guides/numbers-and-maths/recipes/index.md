---
title: Recipes
---

# Recipes: Numbers and maths

Task-focused how-tos. If you know what you want to do but aren't sure how to build it, this is the section to skim.

## Recipes in this section

- **[Round numbers correctly](round-numbers-correctly.ipynb)** — why `round(2.5)` is `2`, how to get the "round half up" most people expect, rounding to a number of decimal places or significant figures, and rounding money exactly.
- **[Handle money with Decimal](handle-money-with-decimal.ipynb)** — the end-to-end pattern for currency: build `Decimal`s from strings, do exact arithmetic, `quantize` to two places with a chosen rounding rule, and never let a `float` near it.
- **[Format numbers for display](format-numbers-for-display.ipynb)** — thousands separators, fixed decimal places, percentages, scientific notation, padding and alignment, signs, and other number formats with f-strings.
- **[Avoid common number mistakes](avoid-common-number-mistakes.md)** — a catalogue of the traps: float equality, `Decimal(0.1)` versus `Decimal('0.1')`, mixing `Decimal` and `float`, `nan` comparisons, lossy `sum`, and more.
