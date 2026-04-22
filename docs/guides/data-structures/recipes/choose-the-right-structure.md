# Choose the right data structure

**The question.** You've got data you need to store, and more than one container could plausibly hold it. List? Dict? Set? Tuple? `Counter`? `namedtuple`? You want a decision short enough to make in your head, and long enough to be right most of the time.

The short version: ask what your **primary operation** is. Lookups by key → dict. Membership tests → set. Ordered items → list (if mutable) or tuple (if fixed). Then the edge cases fall out.

## The answer

| Primary operation | Structure | Syntax |
| --- | --- | --- |
| Walk an ordered sequence | `list` | `[1, 2, 3]` |
| Walk a fixed sequence | `tuple` | `(1, 2, 3)` |
| Look up by key | `dict` | `{'a': 1}` |
| Test membership | `set` | `{1, 2, 3}` |
| Count occurrences | `collections.Counter` | `Counter(items)` |
| Group items by category | `dict` of `list` | `{cat: [...]}` |
| Named fields, immutable | `collections.namedtuple` or `dataclass(frozen=True)` | — |
| Many database-style records | `list` of `dict` (or list of dataclasses) | — |

When in doubt, start with `list` or `dict`. They cover the majority of everyday cases, and refactoring to a more specialised structure later is rarely painful.

## Why each one earns its place

**`list`** is the general-purpose ordered container. Appending, indexing, and iterating are all cheap. Reach for it whenever you just need "a bunch of things, in order" and you don't know in advance how many you'll need.

**`tuple`** is a list that doesn't change. Use it for fixed heterogeneous records (`(width, height)`), for return values with a fixed shape, and anywhere you want a dict key — tuples are hashable; lists aren't.

**`dict`** is the lookup table. Inserting, looking up, and deleting by key are all O(1) on average. Dicts also preserve insertion order (since Python 3.7), so you get a usable ordering for free.

**`set`** is the membership test. `x in a_set` is O(1); `x in a_list` is O(n). Sets also give you the algebra — union, intersection, difference — which is overkill for small collections but a lifesaver for diffing.

**`collections.Counter`** is a `dict` subclass with counting baked in. `Counter(items)` reads items once and records counts; `most_common(3)` gives you the top three. Reach for it whenever "how many of each?" is the answer you want.

**`namedtuple` / frozen `dataclass`** are tuples with names. Use them when you want attribute access (`p.x` instead of `p[0]`) and immutability. For mutable records — or when you want type hints and default values — a regular `dataclass` is the better choice.

## Trade-offs

**Lists are fine for small collections, slow for membership.** Scanning a 10-item list for `x in list` is instant. Scanning a 100 000-item list, a hundred thousand times, is not. Convert to a set (`lookup = set(list)`) when you're about to do repeated membership checks.

**Sets don't preserve order.** `set([1, 2, 3])` might iterate as `{3, 1, 2}` or any other order. If order matters, stay with a list and deduplicate via `dict.fromkeys(items)` (preserves insertion order).

**Tuples are immutable but shallow.** `(1, [2])` can still have its inner list mutated — the outer tuple is frozen, the inner list isn't. For genuine immutability, use `frozenset` for sets and a frozen `dataclass` plus `tuple`-only fields.

**Don't over-engineer.** A `dict` is often a fine stand-in for a class in a small script. Promote it to a `dataclass` when the shape starts appearing in multiple places or when you need validation — not before.

## Related reading

- [Convert between data structures](convert-between-structures.ipynb) — once you've picked one shape and realise you need another.
- [Merge and compare dictionaries](merge-and-compare-dictionaries.ipynb) — the most common dict manipulations.
- [Work with nested structures](work-with-nested-structures.ipynb) — when one level of container isn't enough.
