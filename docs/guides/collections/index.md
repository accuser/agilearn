---
title: Collections
---

# Collections

The built-in `list`, `dict`, `set`, and `tuple` cover most needs, but the standard-library `collections` module adds a handful of specialised containers that make common jobs shorter, clearer, and often faster. Counting things, grouping things, working efficiently at both ends of a sequence, giving tuple fields names — each has a purpose-built type that turns several lines of fiddly code into one obvious one.

This guide covers the five you'll actually reach for — `Counter`, `defaultdict`, `deque`, `namedtuple`, and the pair `OrderedDict`/`ChainMap` — and, just as importantly, *when* each is the right tool over a plain `dict` or `list`.

## Sections

- **[Learn](learn/)** — four notebooks: counting with `Counter`, grouping with `defaultdict`, fast double-ended sequences with `deque`, and named records with `namedtuple` (plus `OrderedDict` and `ChainMap`).
- **[Recipes](recipes/)** — counting and tallying, grouping items by a key, building queues and sliding windows, and the mistakes these containers invite.
- **[Reference](reference/)** — `Counter`/`defaultdict`, `deque`, and `namedtuple`/`OrderedDict`/`ChainMap` lookups.
- **[Concepts](concepts/)** — essays on why specialised containers exist at all, and how to choose the right one.

New to the topic? Start with [Learn → Counter](learn/01-counter.ipynb). Here for a specific task? [Recipes](recipes/) is task-focused and [Reference](reference/) is for lookups. This guide builds directly on [Data structures](../data-structures/index.md).
