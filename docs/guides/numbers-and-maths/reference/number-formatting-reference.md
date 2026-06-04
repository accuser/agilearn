---
title: Number formatting reference
---

# Number formatting reference

The number side of the format mini-language, used in f-strings and `format()`: `f'{value:spec}'`. For text formatting (alignment of strings, etc.) see the [string processing guide](../../string-processing/index.md); this page is the numeric part.

## The spec, in order

```
[[fill]align][sign][#][0][width][grouping][.precision][type]
```

Every part is optional. A full example: `f'{x:>+12,.2f}'` — right-aligned, forced sign, width 12, comma groups, 2 decimals, fixed-point.

## Type codes

| Type | Meaning | `1234.5` → | `255` → |
| --- | --- | --- | --- |
| `f` / `F` | fixed-point | `f'{1234.5:.2f}'` → `1234.50` | — |
| `e` / `E` | scientific | `f'{1234.5:.2e}'` → `1.23e+03` | — |
| `g` / `G` | general (sig. figs, trims zeros) | `f'{1234.5:.3g}'` → `1.23e+03` | — |
| `%` | percent (×100, adds `%`) | `f'{0.1234:.1%}'` → `12.3%` | — |
| `n` | locale-aware number | varies by locale | — |
| `d` | decimal integer | — | `f'{255:d}'` → `255` |
| `b` | binary | — | `f'{255:b}'` → `11111111` |
| `o` | octal | — | `f'{255:o}'` → `377` |
| `x` / `X` | hex (lower/upper) | — | `f'{255:x}'` → `ff` |
| `c` | Unicode character | — | `f'{65:c}'` → `A` |

No type given: ints format as `d`, floats use a `repr`-like general form, `Decimal` keeps its own representation.

## Precision (`.N`)

| Spec | On | Result |
| --- | --- | --- |
| `.2f` | `3.14159` | `3.14` — decimal places |
| `.3g` | `3.14159` | `3.14` — significant figures |
| `.0f` | `2.7` | `3` — no decimals (rounds half to even) |

Precision means *decimal places* for `f`/`e`/`%`, but *significant figures* for `g`.

## Grouping (thousands)

| Spec | On `1234567` | Result |
| --- | --- | --- |
| `,` | | `1,234,567` |
| `_` | | `1_234_567` |
| `,.2f` | `1234567.5` | `1,234,567.50` |

`_` also works with `b`/`o`/`x` to group bits/digits: `f'{255:_b}'` → `1111_1111`.

## Sign

| Spec | `42` → | `-42` → |
| --- | --- | --- |
| `-` (default) | `42` | `-42` |
| `+` | `+42` | `-42` |
| (space) | ` 42` | `-42` |

A leading space reserves the sign column so positives and negatives align.

## Width, fill, alignment, and `0`

| Spec | Result | Notes |
| --- | --- | --- |
| `>8` | `␣␣␣␣1234` | right-align in width 8 (numbers' default) |
| `<8` | `1234␣␣␣␣` | left-align |
| `^8` | `␣␣1234␣␣` | centre |
| `08` | `00001234` | zero-pad to width 8 |
| `08.2f` | `01234.50` | zero-pad a fixed-point number |
| `*>8` | `****1234` | custom fill `*`, right-aligned |
| `#x` | `0xff` | `#` adds the base prefix (`0b`/`0o`/`0x`) |

`0` before the width is shorthand for fill `0` with sign-aware padding; prefer it over `0>` for numbers so the minus sign stays left of the zeros.

## Common recipes

| Goal | Spec | Example output |
| --- | --- | --- |
| Money | `,.2f` | `1,234,567.89` |
| Percentage, 1 dp | `.1%` | `12.3%` |
| Fixed 3 dp | `.3f` | `3.142` |
| Scientific, 2 dp | `.2e` | `1.23e+03` |
| Hex byte, padded | `02x` | `0f` |
| Right-aligned column | `>10,.2f` | `␣␣1,234.50` |

Specs can be built dynamically: `f'{x:.{places}f}'` substitutes `places` first, so precision can come from a variable.
