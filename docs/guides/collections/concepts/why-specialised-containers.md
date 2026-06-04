---
title: Why specialised containers
---

# Why specialised containers

You can do almost anything with a `list` and a `dict`. So why does the standard library ship a `Counter`, a `deque`, a `namedtuple`? The honest answer is that you *don't strictly need* them — but reaching for the right one makes code that is shorter, clearer, and sometimes dramatically faster. This essay is about what that "right one" actually buys you, because the gains come in two very different flavours: performance and expression.

## The performance argument: not all O(1) is equal

Start with the one case where the difference is not a matter of taste. A `list` and a `deque` look interchangeable — both hold an ordered sequence — but they're built on different foundations, and that foundation shows at the front.

A `list` is a contiguous block of memory. Appending at the end is cheap: usually there's spare room, and when there isn't, the list grows in amortised constant time. But removing or inserting at the *front* means every other element has to shuffle along by one position to fill or open the gap. That's O(n) — proportional to the length. Do it once and you won't notice. Do it in a loop, draining a queue of a million items with `pop(0)`, and you've written an O(n²) algorithm by accident: a million removals, each shifting up to a million elements.

A `deque` is built as a doubly-linked structure of blocks, so it has a genuine handle on both ends. `appendleft` and `popleft` are O(1) no matter how long it is. The [deque notebook](../learn/03-deque.ipynb) shows the gap on a modest workload — often a hundredfold. This isn't a micro-optimisation; it's the difference between linear and quadratic, which is the difference between "instant" and "hangs" as the data grows. When a data structure's *shape* matches your access pattern, you get the right complexity for free.

`Counter` and `defaultdict` carry smaller but real performance wins too — counting and grouping in C-backed methods rather than Python-level `if key in d` dances — but their bigger contribution is the second flavour.

## The expression argument: code that says what it means

The deeper reason these types exist is readability. Compare counting words by hand:

```python
counts = {}
for word in text.split():
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
```

with the version that names the intent:

```python
counts = Counter(text.split())
```

Both produce the same dict. But the second one doesn't just *do* the counting — it *announces* it. A reader sees `Counter` and instantly knows the shape of what follows: this is a tally, `most_common` is probably nearby, the values are counts. The manual version makes them reverse-engineer that intent from four lines of bookkeeping. The specialised type turns a pattern into a noun.

The same is true across the module. `defaultdict(list)` says "I'm grouping". A `namedtuple` called `Point(x=3, y=4)` says what a bare `(3, 4)` cannot — which number is which — and a stray `point.x` in code two screens away is self-explanatory where `point[0]` is a small puzzle. `ChainMap(overrides, defaults)` says "layered lookup, first wins" in a single expression. Each replaces a comment ("# this dict is really a frequency count") with a type that *is* the comment, and can't drift out of date.

## Making illegal states harder to reach

There's a subtler benefit hiding in `namedtuple`'s immutability. A coordinate stored as a mutable list `[3, 4]` can be appended to, reordered, or have an element deleted — none of which makes sense for a point, but all of which the type permits. A `namedtuple` simply can't be mutated, so a whole class of bugs ("who changed this point?") becomes impossible rather than merely discouraged. Choosing a more constrained type is a way of encoding what you *won't* do, so the compiler-in-your-head — and your reader — has less to worry about.

## The cost, and the balance

None of this is free of trade-offs. A `namedtuple` is rigid where a `dict` is flexible; a `deque` is slow at random middle access where a `list` is fast; importing `Counter` is one more name than `{}`. The specialised types are sharper tools, and sharper tools are less general. The skill isn't "always use the fancy container" — it's recognising the *pattern* in front of you (tallying, grouping, queueing, a fixed record) and reaching for the type built for it.

That recognition is most of the value. Once you see "I'm counting" rather than "I'm writing a loop over a dict", the right container is obvious, the code gets shorter, and quite often it gets faster too — a rare case where clarity and performance pull in the same direction. The [choosing a container](choosing-a-container.md) essay turns the recognition into a quick decision.
