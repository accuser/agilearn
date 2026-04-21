---
title: Learn
---

# Learn: Iterators and generators

Four notebooks, in order. Each is self-contained but they build on each other — if you work through them in sequence you'll cover the whole topic once.

## Notebooks in this section

1. **[The iteration protocol](01-iteration-protocol.ipynb)** — what actually happens when you write a `for` loop. `iter()`, `next()`, `StopIteration`, and why any object with these behaviours fits into Python's iteration machinery.
2. **[Generator functions](02-generator-functions.ipynb)** — the `yield` keyword. How generator functions turn sequential code into iterables, pausing between values instead of computing them all at once.
3. **[Generator expressions and `itertools`](03-generator-expressions-and-itertools.ipynb)** — inline generator syntax (`(x*2 for x in xs)`) and the standard-library toolkit of iterator combinators.
4. **[Custom iterators](04-custom-iterators.ipynb)** — writing iterator classes when a generator function isn't the right shape. The `__iter__`/`__next__` pair and when you'd reach for them.

After these, the [Recipes](../recipes/) cover task-focused applications and the [Reference](../reference/) has quick lookups for the iterator protocol, generator syntax, and `itertools`.
