---
title: Laziness and memory
---

# Laziness and memory

Lazy evaluation is one of those ideas that sounds like a micro-optimisation and turns out to be a different way of thinking about data. Once you start writing pipelines lazily, you stop asking "will this fit in memory?" and start asking "what's the consumer going to do with the values?"

This essay is about *why* that shift matters, when it earns its keep, and where the trade-offs show up.

## The eager default

Most code most of the time is eager. You compute a list, you pass it to a function, the function does something with it. The values exist; they sit in memory; nothing is hidden.

```python
words = read_words(path)              # all words now in memory
filtered = [w for w in words if len(w) > 5]
counts = Counter(filtered)
top_ten = counts.most_common(10)
```

This is fine for small inputs and the easiest code to reason about. Each variable is a thing you can print, slice, index, iterate twice. There's no surprise about *when* anything happens — it happens on the line you wrote.

The downsides arrive quietly:

- The `words` list materialises every word in the file before you do anything with it. If the file is 10 GB, you OOM before you've started.
- The `filtered` list materialises all the long ones before you count them. If 90% of the words are long, you've allocated nine times more than you need at peak.
- The intermediate lists are thrown away after the next step uses them — you paid for them and then discarded them.

For a small file, none of this matters. For a large file, all three add up.

## What laziness changes

A lazy pipeline reorganises the same logic so that values flow through one at a time. The total amount of work is the same; the *peak* memory is bounded by the cost of the running stages, not the size of the input.

```python
def words_in(path):
    with open(path) as f:
        for line in f:
            for w in line.split():
                yield w

counts = Counter(w for w in words_in(path) if len(w) > 5)
top_ten = counts.most_common(10)
```

Trace the values: the consumer (`Counter`) calls `next()` on the genexp, which calls `next()` on `words_in`, which reads one line and yields one word. `Counter` increments its dictionary by one entry, then asks for the next word. The `words_in` generator yields the next word; `Counter` increments again. There is never a "list of all words" in memory — only the current word, and the running `Counter` (whose size is bounded by the *vocabulary*, not the file).

The shape of the computation changed. Each value is touched by every stage in the pipeline before the next value is touched at all. This is sometimes called *streaming* and sometimes called *online* processing; both names emphasise the same thing — values move through, they don't pile up.

## When laziness matters

Three distinct wins, often in combination:

**Memory.** The big one. You can process inputs that don't fit in RAM. This is what makes "process a 100 GB log on a laptop" possible.

**Latency.** The first result appears as soon as the first input is processed, not after the whole input has been loaded. If you're searching a large file for the first match (`next(line for line in f if 'ERROR' in line)`), lazy evaluation means you stop reading the file as soon as you find it. An eager `[line for line in f if 'ERROR' in line][0]` reads the whole thing first.

**Composition.** Lazy stages plug into each other without intermediate materialisation. You can build a four-stage pipeline that uses constant memory, then add a fifth stage and it's still constant. Eager pipelines don't compose that way — every stage doubles your peak memory.

## When laziness doesn't help (or actively hurts)

It is easy to over-apply this. Three situations where laziness is the wrong choice:

**You'll iterate the data more than once.** A generator is single-use. If the pipeline ends with `for x in gen: ... ; for x in gen: ...`, the second loop sees nothing. You can either re-build the generator each time (paying the cost twice) or materialise once into a list (no cheaper than being eager from the start).

**The data is small.** A list of a thousand integers fits in 30 KB. The simplicity of eager code is worth more than the negligible memory saving. Reach for laziness when the alternative actually hurts.

**Sorting or random access is required.** `sorted` is fundamentally eager — it has to see every element before it can produce the first one. Same for `len`, slicing, and indexing. If your pipeline ends with a sort, the sort destroys the laziness. The whole-pipeline memory cost becomes O(n) regardless of what came before.

A useful diagnostic: *can a single value be processed end-to-end without looking at any other?* If yes, laziness compounds nicely. If the operation is inherently a "see them all" — sort, group, full statistics — then somewhere in the pipeline you have to materialise.

## The hidden cost — debugging

A lazy pipeline is harder to inspect. Type its name into a REPL and you get `<generator object at 0x...>`, not a list of values. Print it and you don't iterate it; iterate it once and you can't iterate it again. If a stage is buggy, the symptom shows up at the *consumer*, not where the bug lives.

The fix is small but real: insert a `tap` stage that prints values as they pass, or temporarily wrap a stage in `list()` to materialise it for inspection. Once the bug is fixed, take the `list()` back out. This ergonomic friction is one reason eager code stays the default — it's easier to debug, even when it's slower.

## The Python design choice

Python the language committed to laziness in stages. The classic example is the move from Python 2 to Python 3: `range`, `map`, `filter`, `zip`, `dict.keys`, `dict.values`, `dict.items` all became lazy. Python 2's `range(1_000_000)` allocated a million-element list; Python 3's `range(1_000_000)` is a small object you iterate. The conversion broke a lot of code that assumed `range(...)` was a list, but the design judgement — that lazy is the right default for these — was a clear improvement.

You can see the same judgement in `itertools`: every function returns an iterator, never a list. The standard library treats laziness as the default, and asks you to opt back into materialisation with `list(...)` when you actually want it.

## A practical rule

Default to eager for small data and clarity. Switch to lazy when:

- The input could be larger than you want in memory.
- You need streaming behaviour (start producing output before the input is fully read).
- You're composing several transformations and want to avoid intermediate copies.
- You're working with a source that's *intrinsically* lazy (a file, a stream, a database cursor) and materialising it would defeat the point.

Don't switch to lazy when:

- You'll iterate the result more than once.
- You need indexing, sizing, or random access.
- The operation forces materialisation anyway (sort, full reduction over a finite known set).

Laziness is a tool, not a virtue. The right answer for any specific bit of code depends on what comes next.
