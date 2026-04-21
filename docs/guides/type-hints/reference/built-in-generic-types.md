---
title: Built-in generic types
---

# Built-in generic types

The lowercase built-in forms for typing collections. All of these work from Python 3.9 onwards. Before 3.9, use the capitalised equivalents from `typing` (`List`, `Dict`, etc.).

## The concrete built-ins

| Annotation | What it is |
| --- | --- |
| `list[T]` | A mutable list of `T` |
| `tuple[T, ...]` | Variable-length tuple of `T` |
| `tuple[A, B, C]` | Fixed-length tuple, one type per position |
| `set[T]` | A set of `T` |
| `frozenset[T]` | An immutable set of `T` |
| `dict[K, V]` | Dict mapping `K` to `V` |
| `type[T]` | The class `T` itself (not an instance) |

## The abstract container types

From `collections.abc` (preferred) or `typing` (legacy). These describe what an object *supports* rather than what concrete type it is — accepting them as parameters makes a function flexible.

### Iterable hierarchy

| Type | Supports | Examples |
| --- | --- | --- |
| `Iterable[T]` | `for x in xs:` (one pass) | anything iterable |
| `Iterator[T]` | `next(it)`, also iterable | generators, `iter(...)` |
| `Collection[T]` | `len`, `in`, iteration | any sized iterable |
| `Sequence[T]` | indexing, slicing | `list`, `tuple`, `range`, `str`, `bytes` |
| `MutableSequence[T]` | `.append`, `.insert`, item assignment | `list`, `bytearray` |
| `Set[T]` | `&`, `\|`, `-`, `<=`, etc. | `set`, `frozenset` |
| `MutableSet[T]` | `.add`, `.discard` | `set` only |

### Mapping hierarchy

| Type | Supports | Examples |
| --- | --- | --- |
| `Mapping[K, V]` | `m[k]`, `.get`, `.keys`, iteration | any dict-like |
| `MutableMapping[K, V]` | `m[k] = v`, `.update`, `.pop` | `dict`, `defaultdict`, `OrderedDict` |

### Async versions

| Type | Meaning |
| --- | --- |
| `AsyncIterable[T]` | `async for x in xs:` |
| `AsyncIterator[T]` | Async iterator (has `__anext__`) |
| `Awaitable[T]` | Can be `await`-ed to produce `T` |
| `Coroutine[Y, S, R]` | What an `async def` returns — usually just use `-> R` on the function |

## Choosing between abstract and concrete

**Rule of thumb:**

- For **parameters**, pick the most abstract type that supports what your function actually does. If you only iterate, use `Iterable[T]`. If you index, use `Sequence[T]`. If you mutate, use `MutableSequence[T]` or `list[T]`.
- For **return types**, use the concrete type so callers know what they're getting. Returning `Iterable[T]` is honest if the return could be a generator, but often less helpful than returning `list[T]`.

```python
from collections.abc import Iterable

# Good: flexible input, concrete output
def uppercase_all(items: Iterable[str]) -> list[str]:
    return [s.upper() for s in items]
```

## Legacy `typing` equivalents

For Python < 3.9, every built-in generic has a capitalised equivalent in `typing`:

| 3.9+ | `typing` equivalent |
| --- | --- |
| `list[T]` | `List[T]` |
| `dict[K, V]` | `Dict[K, V]` |
| `tuple[T, ...]` | `Tuple[T, ...]` |
| `set[T]` | `Set[T]` |
| `frozenset[T]` | `FrozenSet[T]` |
| `type[T]` | `Type[T]` |

The capitalised forms still work everywhere but are deprecated for new code from 3.9 onwards.

## Custom generic types

To make your own class generic, subclass `Generic[T]` (or use the 3.12+ syntax):

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

ints: Stack[int] = Stack()
ints.push(1)
ints.push(2)

# On 3.12+, equivalent without the TypeVar import:
# class Stack[T]:
#     ...
```

The `Generic[T]` base class is what makes `Stack[int]` and `Stack[str]` legal syntax.

## Variance notes

Mutable containers are **invariant** — `list[Animal]` is not a supertype or subtype of `list[Dog]`, even if `Dog` is a subclass of `Animal`. This is because mutation would let you put a non-Dog into a list that's supposed to be Dog-only.

Abstract **read-only** containers like `Sequence` and `Mapping` are **covariant** — `Sequence[Animal]` accepts `Sequence[Dog]`. This is one of the reasons the rule of thumb above works: abstract types let the type-checker be more permissive about what matches.

Most of the time you don't need to think about variance — accept abstract types for parameters and it just works.
