---
title: Learn
---

# Learn: Collections

Four notebooks, in order. Each is self-contained, but together they cover the whole module — one container per notebook (with the smaller `OrderedDict` and `ChainMap` folded into the last).

## Notebooks in this section

1. **[Counter](01-counter.ipynb)** — counting hashable things. Building a `Counter` from any iterable, `most_common`, the arithmetic operators (`+`, `-`, `&`, `|`), `update`/`subtract`, `total`, and `elements`.
2. **[defaultdict](02-defaultdict.ipynb)** — a `dict` that supplies a default for missing keys. The grouping pattern (`list`), the counting pattern (`int`), sets and nesting, and how it compares to `dict.setdefault`.
3. **[deque](03-deque.ipynb)** — a double-ended queue with fast appends and pops at *both* ends. Why `list.pop(0)` is slow, `appendleft`/`popleft`, bounded deques with `maxlen` for sliding windows and history, and `rotate`.
4. **[namedtuple and friends](04-namedtuple-and-friends.ipynb)** — tuples with named fields: defining them, `_replace`, `_asdict`, `_fields`, and how they sit between a tuple and a class. Then `OrderedDict` (what it still offers now that `dict` keeps order) and `ChainMap` (layered lookups for configs and defaults).

After these, the [Recipes](../recipes/) cover task-focused applications and the [Reference](../reference/) has quick lookups for every type.
