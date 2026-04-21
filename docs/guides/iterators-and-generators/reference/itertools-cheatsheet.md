---
title: itertools cheatsheet
---

# `itertools` cheatsheet

The whole `itertools` module on one page. Every function returns an iterator — nothing is materialised unless you call `list(...)` on the result.

```python
import itertools
```

## Infinite iterators

Call these without care — they never stop. Always cap with `islice` or a `break`.

| Function | Yields | Example |
| --- | --- | --- |
| `count(start=0, step=1)` | `start, start+step, start+2*step, …` | `islice(count(10, 2), 3)` → `[10, 12, 14]` |
| `cycle(iterable)` | repeats the iterable forever | `islice(cycle('ab'), 5)` → `['a','b','a','b','a']` |
| `repeat(value, times=None)` | `value` forever, or `times` times | `list(repeat('x', 3))` → `['x','x','x']` |

## Bounding and slicing

| Function | Yields | Example |
| --- | --- | --- |
| `islice(iter, stop)` | first `stop` items | `list(islice('abcdef', 3))` → `['a','b','c']` |
| `islice(iter, start, stop[, step])` | slice semantics for iterators | `list(islice('abcdef', 1, 5, 2))` → `['b','d']` |
| `takewhile(pred, iter)` | yield while `pred(x)` is true, stop at first false | `list(takewhile(lambda x: x<5, [1,2,5,3]))` → `[1,2]` |
| `dropwhile(pred, iter)` | skip while `pred(x)` is true, yield rest | `list(dropwhile(lambda x: x<5, [1,2,5,3]))` → `[5,3]` |

## Combining iterables

| Function | Yields | Example |
| --- | --- | --- |
| `chain(*iterables)` | each iterable end-to-end | `list(chain([1,2], [3,4]))` → `[1,2,3,4]` |
| `chain.from_iterable(iter_of_its)` | flatten one level | `list(chain.from_iterable([[1,2],[3]]))` → `[1,2,3]` |
| `zip_longest(*iters, fillvalue=None)` | parallel; pads short iterables | `list(zip_longest([1,2,3], [10], fillvalue=0))` → `[(1,10),(2,0),(3,0)]` |

Plain `zip` (built-in, not `itertools`) stops at the shortest input; pass `strict=True` to raise on length mismatch.

## Grouping

| Function | Yields | Example |
| --- | --- | --- |
| `groupby(iter, key=None)` | `(key, subiterator)` for each run of adjacent equal keys | `[(k, list(g)) for k,g in groupby('AAABBC')]` → `[('A',['A','A','A']),('B',['B','B']),('C',['C'])]` |

`groupby` only groups *adjacent* equal values. Sort by the same key first if the input isn't already grouped.

## Filtering

| Function | Yields | Example |
| --- | --- | --- |
| `filterfalse(pred, iter)` | items where `pred(x)` is false | `list(filterfalse(lambda x: x%2, [1,2,3,4]))` → `[2,4]` |
| `compress(iter, selectors)` | items where matching selector is truthy | `list(compress('abcd', [1,0,1,0]))` → `['a','c']` |

Plain `filter(pred, iter)` (built-in) is the counterpart: yields items where `pred(x)` is true.

## Running reductions

| Function | Yields | Example |
| --- | --- | --- |
| `accumulate(iter)` | running sum | `list(accumulate([1,2,3,4]))` → `[1,3,6,10]` |
| `accumulate(iter, func)` | running application of `func` | `list(accumulate([3,1,4,1,5,9], max))` → `[3,3,4,4,5,9]` |
| `accumulate(iter, func, initial=...)` | as above, prepended with initial | Python 3.8+ |

Common `func` choices: `operator.mul` (running product), `max`, `min`, `lambda a,b: a+b` (explicit).

## Duplicating and branching

| Function | Yields | Example |
| --- | --- | --- |
| `tee(iter, n=2)` | `n` independent iterators over the same stream | `a, b = tee(iter_of_values)` |

`tee` buffers values between the branches. If they're consumed at very different speeds, memory grows. Don't `tee` a stream that doesn't fit in memory.

## Combinatoric

| Function | Yields | Example |
| --- | --- | --- |
| `product(*iters, repeat=1)` | Cartesian product (n-tuples) | `list(product('ab', [1,2]))` → `[('a',1),('a',2),('b',1),('b',2)]` |
| `permutations(iter, r=None)` | r-length ordered arrangements | `list(permutations('abc', 2))` → `[('a','b'),('a','c'),('b','a'),('b','c'),('c','a'),('c','b')]` |
| `combinations(iter, r)` | r-length sorted subsets, no repeats | `list(combinations('abc', 2))` → `[('a','b'),('a','c'),('b','c')]` |
| `combinations_with_replacement(iter, r)` | r-length sorted subsets, with repeats | `list(combinations_with_replacement('abc', 2))` → `[('a','a'),('a','b'),…,('c','c')]` |

## Starmap

| Function | Yields | Example |
| --- | --- | --- |
| `starmap(func, iter_of_tuples)` | `func(*args)` for each `args` in the iterable | `list(starmap(pow, [(2,3),(3,2)]))` → `[8,9]` |

Equivalent to `(func(*args) for args in iter_of_tuples)`. Handy with `zip`: `list(starmap(mult, zip(xs, ys)))`.

## Mental map

If you want to … | use |
| --- | --- |
| Limit an infinite iterator to `n` items | `islice(it, n)` |
| Concatenate several iterables | `chain(a, b, c)` |
| Flatten one level of nesting | `chain.from_iterable(nested)` |
| Running total / product / max | `accumulate(it[, func])` |
| Group adjacent equal items | `groupby(it, key=...)` |
| Pair up with different-length fallback | `zip_longest(a, b, fillvalue=…)` |
| All combinations of inputs | `product(a, b, c)` |
| Sorted subsets | `combinations(it, r)` |
| All orderings | `permutations(it, r)` |
| Branch an iterator | `tee(it, n)` |
| Skip a prefix matching a predicate | `dropwhile(pred, it)` |
| Take a prefix matching a predicate | `takewhile(pred, it)` |

Each of these appears in the [Recipes](../recipes/) section with worked examples.
