---
title: Recipes
---

# Recipes: Collections

Task-focused how-tos. If you know what you want to do but aren't sure how to build it, this is the section to skim.

## Recipes in this section

- **[Count and tally items](count-and-tally-items.ipynb)** — frequency counts from any iterable, the top-N most common, counting with a condition, and combining or differencing counts with `Counter` arithmetic.
- **[Group items with defaultdict](group-items-with-defaultdict.ipynb)** — turn a flat list into a `{key: [items]}` mapping, group into sets, build an index, and nest groups — plus when `setdefault` or `itertools.groupby` fits better.
- **[Build a queue or sliding window](build-a-queue-or-sliding-window.ipynb)** — a FIFO queue, a bounded history of the last N items, a moving average over a window, and an undo stack — all with `deque`.
- **[Avoid common collections mistakes](avoid-common-collections-mistakes.md)** — a catalogue of the traps: `defaultdict` creating keys when you only read, dropped items from `maxlen`, `Counter` quirks, namedtuple immutability, and reaching for a `list` where a `deque` belongs.
