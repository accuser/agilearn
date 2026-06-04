---
title: Choosing a container
---

# Choosing a container

The `collections` module gives you several ways to store things, and the built-in `dict` and `list` overlap with all of them. This essay is a practical guide to picking the right one — not by memorising a table, but by asking what you're actually doing with the data. In almost every case a single question settles it.

## Start with the built-ins

The honest default is: **use a `list` or a `dict` until you have a reason not to.** They're flexible, universally understood, and fast enough for the overwhelming majority of code. The specialised containers earn their place only when a specific pattern shows up — and the rest of this essay is really a list of those patterns and the type each one signals. If none of them matches, the built-in is the right answer.

## "I'm counting how often things occur" → `Counter`

The tell is that your values are *tallies* — you're incrementing, asking "how many", or wanting the most common. The moment you'd otherwise write `if x in d: d[x] += 1 else: d[x] = 1`, you want a `Counter`. It also gives you `most_common`, multiset arithmetic, and zero-for-missing reads, none of which a hand-rolled dict offers for free. If you're only ever counting, don't reach for `defaultdict(int)` — `Counter` is the same idea with a better toolkit.

## "I'm grouping items into buckets" → `defaultdict`

The tell is a value that *accumulates* — a list you append to, a set you add to, a running sum. `defaultdict(list)` is the canonical grouping tool; `defaultdict(set)` when buckets should dedupe; `defaultdict(int)` for sums. The decision between `defaultdict` and a plain dict's `setdefault` is minor and stylistic: `defaultdict` reads better when one dict is built up consistently through a function, `setdefault` when it's a one-off or you want the result to stay an ordinary dict. The one caveat that should steer you back to `dict`/`get` is read-heavy code where accidental key creation would be a problem.

## "I'm working at the ends of a sequence" → `deque`

The tell is a *queue* or a *window*: you add at one end and remove from the other, or you keep only the most recent N. If your code contains `list.pop(0)` or `list.insert(0, x)`, that's the signal to switch — those are O(n), and a `deque`'s end-operations are O(1). Add `maxlen` when you want a self-trimming window or ring buffer. The flip side: if you mostly index into the middle (`x[i]` for arbitrary `i`) or do random insertion, stay with a `list` — that's where it's faster.

## "I have a small fixed record" → `namedtuple` (or a dataclass)

The tell is a clutch of related values that travel together and have a fixed shape — a coordinate, an RGB colour, a parsed row. A bare tuple works but `point[0]` is opaque; a dict works but is mutable and heavier. A `namedtuple` gives named, immutable fields that still behave as a tuple. The choice between it and a `@dataclass` comes down to two questions: do you need it to be *mutable*, and do you want *methods*? If yes to either, use a dataclass; if it's a small immutable value that should compare and unpack like a tuple, use a `namedtuple`. The [classes guide](../../classes-and-objects/index.md) develops this comparison.

## "I have layered settings to look up" → `ChainMap`

The tell is *precedence*: several sources of the same keys — command-line over environment over defaults — and you want a lookup that returns the highest-priority value without merging copies. `ChainMap` is the niche but exact fit. If you only need a one-time merge and don't care about layers afterwards, a plain `{**defaults, **overrides}` is simpler; reach for `ChainMap` when the layers must stay distinct (so you can change one without disturbing the others).

## A note on `OrderedDict`

Since Python 3.7 a plain `dict` keeps insertion order, so `OrderedDict` is no longer the way to get ordering — a `dict` already has it. Choose `OrderedDict` only for its genuine extras: `move_to_end`, popping from the front, or order-sensitive equality (as in an LRU cache). For everything else, the plain `dict` is the right call.

## The decision in one pass

| What you're doing | Reach for |
| --- | --- |
| nothing special yet | `list` / `dict` |
| counting occurrences, ranking by frequency | `Counter` |
| grouping/accumulating into buckets | `defaultdict` (or `setdefault`) |
| queue, or "last N" window | `deque` (with `maxlen` for the window) |
| small fixed immutable record | `namedtuple` |
| record needing mutation or methods | `@dataclass` |
| layered lookup with precedence | `ChainMap` |
| ordering *plus* reordering/front-pop | `OrderedDict` |

Run down the list, take the first row that matches what you're actually doing, and you'll almost always land on the right container — and on code that announces its intent to the next reader. When nothing past the first row fits, that's not a failure: the built-ins are a fine default, and [why specialised containers](why-specialised-containers.md) explains what the others add when one does fit.
