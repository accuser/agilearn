---
title: Avoid common iterator mistakes
---

# Avoid common iterator mistakes

A catalogue of the gotchas. Most of these are consequences of two facts: iterators are *consumed once*, and generators only do work when you *pull* values.

## 1. Iterating an iterator twice

```python
it = iter([1, 2, 3])

first = sum(it)          # 6
second = sum(it)         # 0  ← already exhausted
```

The second `sum` returns the empty-sum value (0) without raising. The fix: keep the *iterable* and call `iter()` again, or materialise into a list.

```python
xs = [1, 2, 3]
first  = sum(xs)         # 6
second = sum(xs)         # 6  ← lists are re-iterable
```

If your "iterable" is actually a generator function, *re-call the function* each time:

```python
def evens(n):
    for x in range(n):
        if x % 2 == 0:
            yield x

print(sum(evens(10)))    # works
print(sum(evens(10)))    # call again — fresh generator
```

## 2. Mutating a list while iterating it

```python
items = [1, 2, 3, 4, 5]
for x in items:
    if x % 2:
        items.remove(x)        # bug — skips elements
print(items)                   # [2, 3, 4]  ← '3' survived!
```

Iterators over mutable sequences hold an *index* internally. Removing elements shifts that index out from under the loop. Same problem with `dict` and `set` — adding or removing keys mid-iteration raises `RuntimeError: dictionary changed size during iteration`.

The fix: build a new sequence rather than mutating in place.

```python
items = [x for x in items if x % 2 == 0]
```

Or iterate over a copy:

```python
for x in list(items):
    if x % 2:
        items.remove(x)
```

## 3. `return` inside a generator function (not what you think)

A `return` from a generator function does **not** return a value to the caller. It stops iteration. If you `return value`, the value is attached to the `StopIteration` exception, but `for` loops discard it.

```python
def first_n(it, n):
    for i, x in enumerate(it):
        if i >= n:
            return         # stops the generator
        yield x

print(list(first_n([1,2,3,4,5], 3)))   # [1, 2, 3]
```

If you wanted to compute and *return* a final value, you'd write a regular function (`def total(it): return sum(it)`), not a generator.

## 4. Late binding in generator expressions

The expression's loop variable is evaluated lazily. So if you build a list of generators that close over an outer-scope variable, every generator sees the *current* value at consumption time, not the value when it was created.

```python
gens = []
for i in range(3):
    gens.append((i + x for x in range(2)))

for g in gens:
    print(list(g))
```

Output:

```
[2, 3]
[2, 3]
[2, 3]
```

Each generator sees the *final* value of `i` (which is 2), because the inner expression `i + x` is evaluated when each generator is consumed — *after* the loop has moved `i` to its final value.

The fix: bind early with a default argument:

```python
gens = []
for i in range(3):
    gens.append(((j + x) for j, x in [(i, x) for x in range(2)]))
```

Or use a helper function so `i` is captured per call:

```python
def make_gen(i):
    return (i + x for x in range(2))

gens = [make_gen(i) for i in range(3)]
for g in gens:
    print(list(g))
# [0, 1]
# [1, 2]
# [2, 3]
```

This bites people enough to know it: anything captured by reference in a closure is captured *by reference*, not by value.

## 5. `try`/`finally` around code containing `yield`

When a generator is partially consumed and then garbage collected, Python triggers the `finally` block by raising `GeneratorExit` into the generator. If your `finally` does cleanup (closing a file, releasing a lock), that's fine — but it *only* fires when the generator is closed. If callers might hold the generator open indefinitely, the cleanup is delayed.

```python
def reader(path):
    f = open(path)
    try:
        for line in f:
            yield line
    finally:
        f.close()

# OK — for loops close the generator on exit
for line in reader('/tmp/data'):
    if line.startswith('#'):
        break    # generator closed here, file closed by finally

# Bad — first 5 lines, file stays open until gc collects the generator
g = reader('/tmp/data')
first_five = [next(g) for _ in range(5)]
```

Two fixes:

- Wrap the consumer in a `with closing(...)` (`from contextlib import closing`).
- Or restructure so the file is opened by the *caller* and the generator just iterates over it.

## 6. Calling `iter()` on a callable instead of using `iter(callable, sentinel)`

`iter(obj)` requires `obj` to be iterable (it has `__iter__`). Functions are not iterable, so `iter(some_func)` raises `TypeError`. The two-argument form `iter(callable, sentinel)` is what you want for "call this function repeatedly until it returns the sentinel".

```python
# Wrong
iter(input)         # TypeError: 'builtin_function_or_method' is not iterable

# Right — read lines from stdin until empty
for line in iter(input, ''):
    process(line)
```

## 7. Treating `range`, `dict.keys()`, etc. as iterators

These are *iterables*, not iterators. They produce a fresh iterator each time you iterate — and they support `len()`, `in`, indexing in some cases. You can iterate them as many times as you like.

```python
r = range(10)
list(r)        # [0, 1, ..., 9]
list(r)        # works again — range is iterable, not iterator

d = {'a': 1, 'b': 2}
keys = d.keys()
list(keys)     # ['a', 'b']
list(keys)     # works again
```

Don't accidentally `iter(...)` them and pass the iterator on — you'll lose re-iteration.

## 8. `next(it)` instead of `next(it, default)`

The one-argument form raises `StopIteration` on exhaustion. In a `for` loop that's fine — the loop handles it. But in your own code, if `StopIteration` leaks out, it can be confusing or trigger PEP 479 errors inside generators.

```python
def first_or(default, iterable):
    return next(iter(iterable), default)    # safer
```

Always use the two-arg form unless you specifically *want* `StopIteration` to propagate.

## 9. `min`/`max`/`sum` on an empty generator

These raise `ValueError` (for `min`/`max`) or return 0 (for `sum`) on empty input. If your generator might yield nothing, decide what you want and supply a default.

```python
result = max(gen, default=None)
result = sum(gen, start=0)             # default
```

## 10. Forgetting to consume the pipeline

A pipeline of generators does no work until something consumes it.

```python
def shouts(xs):
    for x in xs:
        print(f'shouting {x}')         # nothing printed
        yield x.upper()

shouts(['hi', 'there'])                # value discarded; nothing happens
```

You need a consumer:

```python
list(shouts(['hi', 'there']))
# or
for _ in shouts(['hi', 'there']):
    pass
```

## 11. `sorted(...)` is eager — it materialises

`sorted` always returns a list. It can't sort lazily — sorting needs every element. If your input is huge, sorting destroys the constant-memory property of the rest of your pipeline. If you only need the top-`k`, use `heapq.nlargest(k, iterable)` instead.

```python
import heapq
top10 = heapq.nlargest(10, huge_generator())   # constant memory
```

## 12. Re-using a `groupby` group iterator after the outer loop advances

```python
from itertools import groupby
items = [('a', 1), ('a', 2), ('b', 3)]
saved = [(key, group) for key, group in groupby(items, key=lambda p: p[0])]

for key, group in saved:
    print(list(group))     # all empty!
```

Each group iterator is only valid while you're on its iteration. Materialise inside the loop:

```python
saved = [(key, list(group)) for key, group in groupby(items, key=lambda p: p[0])]
```

## 13. Confusing `filter` with `takewhile` / `dropwhile`

`filter(pred, it)` keeps every element matching the predicate, scanning the whole stream. `takewhile(pred, it)` stops at the *first* non-match. Similarly `dropwhile` skips a prefix only.

```python
from itertools import takewhile, dropwhile

xs = [1, 3, 5, 4, 7, 9]
list(filter(lambda x: x % 2, xs))      # [1, 3, 5, 7, 9]  ← all odds
list(takewhile(lambda x: x % 2, xs))   # [1, 3, 5]        ← stops at 4
list(dropwhile(lambda x: x % 2, xs))   # [4, 7, 9]        ← skips prefix
```

If you want "keep until I see X", reach for `takewhile`.
