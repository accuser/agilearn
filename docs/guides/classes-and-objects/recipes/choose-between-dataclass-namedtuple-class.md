---
title: Choose between @dataclass, NamedTuple, and a plain class
---

# Choose between `@dataclass`, `NamedTuple`, and a plain class

When you just want to bundle a few values under a name, you've got three reasonable options. This page is a decision guide — read the summary, then the notes on each trade-off if you want the reasoning.

## The short answer

| Situation | Reach for |
| --- | --- |
| A record type with more than three fields, or that might grow | `@dataclass` |
| A record type you want to be immutable | `@dataclass(frozen=True)` |
| A small immutable pair or triple, often unpacked | `typing.NamedTuple` |
| Dict-shaped data (from JSON, or going into a library that wants a dict) | `typing.TypedDict` |
| Anything with non-trivial behaviour — heavy custom dunders, complex validation, descriptors | Hand-written class |

If you're not sure, use `@dataclass`. It has the widest sweet spot.

## `@dataclass` — the default choice

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    is_admin: bool = False
```

Gives you `__init__`, `__repr__`, and `__eq__` for free. Add parameters to tune behaviour: `frozen=True` for immutability, `slots=True` for smaller memory footprint, `order=True` for comparison operators, `kw_only=True` (3.10+) to require keyword arguments.

Reach for `@dataclass` when:

- The class is primarily data. You have fields, and the methods mostly compute derived values from those fields.
- You have more than two or three fields, or you expect to add fields over time.
- You want validation — add a `__post_init__`.
- You want mutable state. A plain `@dataclass` gives you that. `@dataclass(frozen=True)` gives you an immutable value type.

## `NamedTuple` — small, immutable, tuple-like

```python
from typing import NamedTuple

class Coord(NamedTuple):
    lat: float
    lon: float
```

`NamedTuple` is a genuine tuple with attribute access bolted on. It's immutable, hashable, memory-cheap, and participates in all the tuple-shaped APIs (unpacking, indexing, `==` with plain tuples).

Reach for `NamedTuple` when:

- The type is small — two or three fields. At four or more, a `@dataclass(frozen=True)` reads better.
- The values won't change over an instance's lifetime.
- You'd plausibly unpack it: `lat, lon = coord`.

Avoid `NamedTuple` when:

- You want methods that mutate state. You can't.
- You need inheritance from another class (`NamedTuple` can't inherit from non-NamedTuple bases).
- You care that `Coord(51.5, -0.1) == (51.5, -0.1)` returns `True`. It does, because a `Coord` *is* a tuple — sometimes useful, sometimes a footgun when comparing heterogeneous data.

## `TypedDict` — types for dict-shaped data

```python
from typing import TypedDict

class UserRecord(TypedDict):
    name: str
    email: str
    is_admin: bool
```

`TypedDict` isn't a runtime class at all. It's a hint to type checkers like mypy and pyright. At runtime, a `UserRecord` is just a plain `dict`.

Reach for `TypedDict` when:

- The data comes from somewhere that hands you dicts — JSON responses, config parsers, `csv.DictReader`.
- You're passing data to a library that expects a dict.
- You want type-checker support for the keys but don't want to convert to a class and back.

The [type hints guide](../../type-hints/) covers `TypedDict` in more detail.

## Plain class — when none of the above fits

Hand-write the class when you need behaviour that doesn't fit dataclass field declarations: extensive custom dunders, descriptors, complex construction logic, runtime-generated attributes. If you're reaching here, you probably know why — the default choice is still `@dataclass`.

## A worked comparison

The same data, in each shape:

```python
# @dataclass
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int = 0

# NamedTuple
from typing import NamedTuple

class Book(NamedTuple):
    title: str
    author: str
    pages: int = 0

# TypedDict
from typing import TypedDict

class Book(TypedDict):
    title: str
    author: str
    pages: int

# Plain class
class Book:
    def __init__(self, title, author, pages=0):
        self.title = title
        self.author = author
        self.pages = pages
```

The `@dataclass` version is barely longer than the `NamedTuple`, mutable by default, and scales to any number of fields without ceremony — which is why it's the best default.
