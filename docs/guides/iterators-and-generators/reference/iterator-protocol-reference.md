---
title: Iterator protocol reference
---

# Iterator protocol reference

The two-method contract that powers `for` loops, `list()`, `sum()`, comprehensions, unpacking, `in`, and the `itertools` module.

## The two methods

| Method | On | Returns | Notes |
| --- | --- | --- | --- |
| `__iter__(self)` | Iterables and iterators | An iterator | On an *iterable*, returns a new iterator. On an *iterator*, returns `self`. |
| `__next__(self)` | Iterators only | Next value | Raises `StopIteration` when exhausted. |

Anything with `__iter__` is an *iterable*. Anything with both `__iter__` and `__next__` (where `__iter__` returns `self`) is an *iterator*.

```python
from collections.abc import Iterable, Iterator

isinstance([1, 2, 3], Iterable)   # True
isinstance([1, 2, 3], Iterator)   # False — list is iterable, not an iterator
isinstance(iter([1, 2, 3]), Iterator)  # True
```

## Built-in functions that use the protocol

| Function | What it does |
| --- | --- |
| `iter(obj)` | Calls `obj.__iter__()` and returns the result. |
| `iter(callable, sentinel)` | Returns an iterator that calls `callable()` until it returns `sentinel`. |
| `next(it)` | Calls `it.__next__()`. |
| `next(it, default)` | As above, but returns `default` instead of raising `StopIteration`. |

The two-argument `iter` is useful for "read until done" loops:

```python
# Read 4-byte chunks from a binary file until EOF
for chunk in iter(lambda: f.read(4), b''):
    ...
```

## What `for x in obj:` actually does

```python
_it = iter(obj)
while True:
    try:
        x = next(_it)
    except StopIteration:
        break
    # body
```

This is the de-sugaring. Anything that implements `__iter__` (and ultimately `__next__`) plugs into a `for` loop, comprehensions, unpacking, and the rest.

## `StopIteration`

Raised by `__next__` when there are no more values. Constructors and properties:

| Form | Use |
| --- | --- |
| `raise StopIteration` | Standard — no value attached. |
| `raise StopIteration(value)` | Attaches `value` to `.value`. Picked up by `yield from`. |
| `e.value` | The attached value (if any). |

Inside a generator function, raising `StopIteration` directly is **not** the way to stop — use `return` instead. Since PEP 479 (Python 3.7+), an unhandled `StopIteration` inside a generator is converted to a `RuntimeError` to prevent silent bugs.

```python
def good():
    yield 1
    return        # stops the generator cleanly

def bad():
    yield 1
    raise StopIteration   # RuntimeError — don't do this
```

## Iterable vs iterator — table

| Property | Iterable (e.g. `list`, `dict`, `range`) | Iterator (e.g. `iter([1,2])`, generator object) |
| --- | --- | --- |
| Has `__iter__` | yes — returns a new iterator | yes — returns `self` |
| Has `__next__` | no | yes |
| Re-iterable | yes — fresh iterator each time | no — exhausted after one pass |
| Has `__len__` | usually | rarely |
| Indexable | sometimes (`list`, `tuple`, `range`) | no |

A generator function returns a generator object, which is an iterator (one-shot, no len, no indexing). To get a re-iterable wrapper, write a class whose `__iter__` is a generator method.

## Custom iterator skeleton

```python
class MyIterator:
    def __init__(self, data):
        self._data = data
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self._data):
            raise StopIteration
        value = self._data[self._i]
        self._i += 1
        return value
```

Custom *iterable* (re-iterable) skeleton:

```python
class MyIterable:
    def __init__(self, data):
        self._data = data

    def __iter__(self):
        return MyIterator(self._data)
```

Or, equivalently and more idiomatically, use a generator method:

```python
class MyIterable:
    def __init__(self, data):
        self._data = data

    def __iter__(self):
        for x in self._data:
            yield x
```

## Cheatsheet — common idioms

| Goal | Idiom |
| --- | --- |
| First value or default | `next(iter(it), default)` |
| Whole iterator into a list | `list(it)` |
| Loop with index | `for i, x in enumerate(it):` |
| Pair adjacent items | `zip(it, it[1:])` for sequences; `pairwise(it)` from `itertools` (Python 3.10+) |
| Flatten one level | `itertools.chain.from_iterable(it)` |
| Skip first n | `itertools.islice(it, n, None)` |
| Take first n | `itertools.islice(it, n)` |
| Read callable until sentinel | `iter(callable, sentinel)` |

## Related references

- [`itertools` cheatsheet](itertools-cheatsheet.md) — the standard-library combinators.
- [Generator syntax reference](generator-syntax-reference.md) — `yield`, `yield from`, `.send`/`.close`, generator expressions.
