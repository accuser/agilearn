---
title: Counter and defaultdict reference
---

# `Counter` and `defaultdict` reference

Both are `dict` subclasses — every dict method works. These pages list only what they add.

```python
from collections import Counter, defaultdict
```

## `Counter`

### Construction

| Form | Result |
| --- | --- |
| `Counter(iterable)` | tally each element — `Counter('aab')` → `{'a': 2, 'b': 1}` |
| `Counter(mapping)` | from existing counts — `Counter({'a': 2})` |
| `Counter(**kwargs)` | from keywords — `Counter(a=2, b=1)` |
| `Counter()` | empty |

### Methods and behaviour

| Member | Does |
| --- | --- |
| `c[key]` | the count, or `0` if absent (no `KeyError`, no insertion) |
| `c.most_common([n])` | list of `(item, count)`, highest first; all if `n` omitted |
| `c.total()` | sum of all counts (Python 3.10+) |
| `c.elements()` | iterator repeating each item by its count (ignores ≤ 0) |
| `c.update(iterable_or_mapping)` | **add** counts (not replace) |
| `c.subtract(iterable_or_mapping)` | subtract counts; may go negative |
| `+c` / `-c` | unary: keep positive / keep negative-flipped counts |
| `len(c)` | number of distinct items |

### Arithmetic operators (return a new `Counter`, dropping counts ≤ 0)

| Operator | Meaning | Example on `a=Counter(x=3,y=1)`, `b=Counter(x=1,y=2)` |
| --- | --- | --- |
| `a + b` | add counts | `{'x': 4, 'y': 3}` |
| `a - b` | subtract, keep positives | `{'x': 2}` |
| `a & b` | intersection (min) | `{'x': 1, 'y': 1}` |
| `a \| b` | union (max) | `{'x': 3, 'y': 2}` |

To keep zero/negative results, use the `subtract` **method** instead of `-`.

## `defaultdict`

`defaultdict(default_factory)` — a dict that calls `default_factory()` (a zero-argument callable) to create a value for any missing key, on first access.

### Common factories

| Factory | Missing key becomes | Use for |
| --- | --- | --- |
| `list` | `[]` | grouping items into buckets |
| `int` | `0` | counting / summing |
| `set` | `set()` | grouping unique items |
| `dict` | `{}` | nested mappings |
| `lambda: defaultdict(int)` | a nested defaultdict | multi-level structures |
| custom `lambda: <value>` | that value | any constant default |

### Behaviour

| Aspect | Note |
| --- | --- |
| missing-key **read** | runs the factory and **inserts** the key (unlike `Counter`) |
| `d.default_factory` | the factory; `None` means "behave like a plain dict" (`KeyError`) |
| `in` / `.get(key)` | check without triggering the factory |
| `dict(d)` | a plain `dict` copy — no more auto-creation |

`defaultdict(None)` has no factory, so missing keys raise `KeyError` like an ordinary dict.

## `Counter` or `defaultdict`?

| Want | Use |
| --- | --- |
| frequency counts + ranking | `Counter` |
| count without inserting on read | `Counter` (reads return `0` cleanly) |
| group items into lists/sets | `defaultdict(list)` / `defaultdict(set)` |
| accumulate sums or build nested structures | `defaultdict(int)` / nested `defaultdict` |
