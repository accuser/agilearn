---
title: Dunder methods catalogue
---

# Dunder methods catalogue

The dunder methods you're most likely to implement, grouped by role. This is a reference page — if you're meeting dunders for the first time, start with the [dunder methods tutorial](../learn/02-dunder-methods.ipynb).

## Object representation

| Method | Triggered by | Returns |
| --- | --- | --- |
| `__repr__(self)` | `repr(x)`, `f"{x!r}"`, debuggers, container printing | A debug-friendly string; should ideally look like code that reconstructs the object. |
| `__str__(self)` | `str(x)`, `print(x)`, `f"{x}"` | A user-facing string. Falls back to `__repr__` if not defined. |
| `__format__(self, spec)` | `f"{x:spec}"`, `format(x, spec)` | String formatted according to `spec`. Default delegates to `str()`. |
| `__bytes__(self)` | `bytes(x)` | A `bytes` representation. |

Always implement `__repr__`. Implement `__str__` only when the user-facing form should differ from the debug form.

## Equality and hashing

| Method | Triggered by | Returns |
| --- | --- | --- |
| `__eq__(self, other)` | `x == y` | `True`, `False`, or `NotImplemented` for unknown types. |
| `__ne__(self, other)` | `x != y` | Usually not needed — Python derives it from `__eq__`. |
| `__hash__(self)` | `hash(x)`, `set` and `dict` membership | An `int`. Must be consistent with `__eq__`: equal objects must have equal hashes. |

Defining `__eq__` removes the default `__hash__`. Add `__hash__` back for immutable classes; leave it off for mutable ones.

## Ordering

| Method | Triggered by |
| --- | --- |
| `__lt__(self, other)` | `x < y` |
| `__le__(self, other)` | `x <= y` |
| `__gt__(self, other)` | `x > y` |
| `__ge__(self, other)` | `x >= y` |

Return `True`, `False`, or `NotImplemented`. For the full set, define `__eq__` plus any one of these, then decorate the class with `@functools.total_ordering`.

## Arithmetic

| Method | Triggered by | Right-hand form |
| --- | --- | --- |
| `__add__(self, other)` | `x + y` | `__radd__(self, other)` for `y + x` when `y` doesn't know about `x`. |
| `__sub__` | `x - y` | `__rsub__` |
| `__mul__` | `x * y` | `__rmul__` |
| `__truediv__` | `x / y` | `__rtruediv__` |
| `__floordiv__` | `x // y` | `__rfloordiv__` |
| `__mod__` | `x % y` | `__rmod__` |
| `__pow__` | `x ** y` | `__rpow__` |
| `__matmul__` | `x @ y` | `__rmatmul__` |
| `__neg__(self)` | `-x` | — |
| `__pos__(self)` | `+x` | — |
| `__abs__(self)` | `abs(x)` | — |

There are in-place versions too — `__iadd__`, `__isub__`, and so on — for `x += y` and friends. Define these only when in-place mutation is genuinely different from creating a new object.

## Container behaviour

| Method | Triggered by |
| --- | --- |
| `__len__(self)` | `len(x)` — and gives free truthiness (empty = falsy). |
| `__getitem__(self, key)` | `x[key]`, including slicing when `key` is a `slice` object. |
| `__setitem__(self, key, value)` | `x[key] = value` |
| `__delitem__(self, key)` | `del x[key]` |
| `__contains__(self, item)` | `item in x` |
| `__iter__(self)` | `for i in x`, `iter(x)` |
| `__reversed__(self)` | `reversed(x)` |
| `__missing__(self, key)` | `dict` subclass lookup fallback when key is absent. |

Inheriting from `collections.abc.Sequence`, `MutableSequence`, `Mapping`, or `Set` fills in most of these from a small set of required methods.

## Iteration

| Method | Role |
| --- | --- |
| `__iter__(self)` | Called by `iter(x)`. Should return an iterator (often a fresh one each time). |
| `__next__(self)` | Called by `next(x)`. Raises `StopIteration` when exhausted. Implemented by the iterator, not the iterable. |

The iterable/iterator distinction matters — see the [iterators and generators guide](../../iterators-and-generators/) for when to implement which.

## Context managers

| Method | Triggered by |
| --- | --- |
| `__enter__(self)` | Entering a `with` block. Returns the value bound to the `as` variable. |
| `__exit__(self, exc_type, exc_value, traceback)` | Leaving a `with` block. Return truthy to suppress an exception, falsy (or nothing) to let it propagate. |

For common cases, `contextlib.contextmanager` (with a generator) is lighter than a full class.

## Attribute access

| Method | Triggered by |
| --- | --- |
| `__getattr__(self, name)` | Attribute lookup **when the normal lookup fails**. A fallback. |
| `__getattribute__(self, name)` | **Every** attribute lookup. Rarely implemented — easy to accidentally infinite-loop. |
| `__setattr__(self, name, value)` | Every attribute assignment. Use `super().__setattr__` to actually store. |
| `__delattr__(self, name)` | Every `del x.attr`. |
| `__dir__(self)` | `dir(x)` — controls tab-completion and introspection. |

## Callable and descriptor protocol

| Method | Role |
| --- | --- |
| `__call__(self, ...)` | Makes the instance callable: `x(...)` runs `x.__call__(...)`. Useful for stateful functions. |
| `__get__(self, obj, objtype=None)` | Descriptor protocol — lookup on an instance. Behind `@property`, `@classmethod`, and `@staticmethod`. |
| `__set__(self, obj, value)` | Descriptor protocol — assignment. |
| `__delete__(self, obj)` | Descriptor protocol — `del`. |

## Type conversion

| Method | Triggered by |
| --- | --- |
| `__bool__(self)` | `bool(x)`, truthiness tests. Falls back to `__len__` if not defined. |
| `__int__(self)` | `int(x)` |
| `__float__(self)` | `float(x)` |
| `__complex__(self)` | `complex(x)` |
| `__index__(self)` | Used as an integer index (slicing, `bin()`, `hex()`). Stricter than `__int__`. |

## Lifecycle

| Method | Role |
| --- | --- |
| `__new__(cls, ...)` | Constructs the raw instance. Rarely overridden; subclassing immutable types is the main case. |
| `__init__(self, ...)` | Initialises the instance. The one you override almost always. |
| `__del__(self)` | Called when the instance is garbage-collected. Unreliable timing — prefer context managers for cleanup. |
| `__init_subclass__(cls, ...)` | Called on the parent when a subclass is defined. Useful for registry patterns. |

## Copying and pickling

| Method | Role |
| --- | --- |
| `__copy__(self)` | `copy.copy(x)` — shallow copy. |
| `__deepcopy__(self, memo)` | `copy.deepcopy(x)` — deep copy. |
| `__getstate__(self)` | Return the state to be pickled. |
| `__setstate__(self, state)` | Restore state during unpickling. |
| `__reduce__(self)` | Full pickle-protocol hook; rarely needed. |
