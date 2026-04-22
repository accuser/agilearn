# Choose between @dataclass, NamedTuple, and a plain class

**The question.** You want to bundle a few values under a name and you have four reasonable options: `@dataclass`, `typing.NamedTuple`, `typing.TypedDict`, or a hand-written class. They look similar from ten feet away and behave quite differently up close.

The short answer: default to `@dataclass`. Everything else is a case where the default doesn't fit.

## The answer

| Situation | Reach for |
| --- | --- |
| More than three fields, or likely to grow | `@dataclass` |
| Immutable record | `@dataclass(frozen=True)` |
| Small, immutable, often unpacked (2–3 fields) | `typing.NamedTuple` |
| Dict-shaped data from JSON or config | `typing.TypedDict` |
| Non-trivial behaviour, complex construction, descriptors | Hand-written class |

If you're not sure, use `@dataclass`. It has the widest sweet spot.

## Why `@dataclass` is the default

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    is_admin: bool = False
```

That gives you `__init__`, `__repr__`, and `__eq__` for free. `frozen=True` makes it immutable; `slots=True` shrinks the memory footprint; `order=True` generates comparison operators; `kw_only=True` (3.10+) requires keyword arguments. Reach for it whenever the class is primarily data: the fields are what matter, and the methods mostly compute derived values. `@dataclass` scales to any number of fields without ceremony, which is why it's the safest starting point.

## When `NamedTuple` earns its place

```python
from typing import NamedTuple

class Coord(NamedTuple):
    lat: float
    lon: float
```

`NamedTuple` is a genuine tuple with attribute access bolted on. Immutable, hashable, memory-cheap, participates in tuple-shaped APIs (unpacking, indexing, `==` with plain tuples). Use it when the type is small (two or three fields), the values won't change, and unpacking (`lat, lon = coord`) reads naturally.

Avoid it when you'd ever want to mutate state, inherit from another (non-NamedTuple) class, or when it matters that `Coord(51.5, -0.1) == (51.5, -0.1)` is `True` — sometimes handy, sometimes a footgun.

## When `TypedDict` earns its place

```python
from typing import TypedDict

class UserRecord(TypedDict):
    name: str
    email: str
    is_admin: bool
```

`TypedDict` is a hint to type checkers. At runtime, a `UserRecord` is a plain `dict`. Use it when data comes from somewhere that hands you dicts (JSON, `csv.DictReader`, config parsers) and you don't want to convert into and out of a class. The [type hints guide](../../type-hints/) covers it in more detail.

## When a hand-written class earns its place

Reach for a plain class when you need behaviour that doesn't fit dataclass field declarations: complex construction, heavy custom dunders, descriptors, runtime-generated attributes. If you're writing one of these, you probably know why — and the default for most everyday cases is still `@dataclass`.

## Trade-offs

**The same four fields, four ways:**

```python
# @dataclass — mutable, extensible, ~3 lines
@dataclass
class Book:
    title: str
    author: str
    pages: int = 0

# NamedTuple — immutable, tuple-compatible, similar size
class Book(NamedTuple):
    title: str
    author: str
    pages: int = 0

# TypedDict — typed view of a dict, no runtime class
class Book(TypedDict):
    title: str
    author: str
    pages: int

# Plain class — full control, full boilerplate
class Book:
    def __init__(self, title, author, pages=0):
        self.title = title
        self.author = author
        self.pages = pages
```

The `@dataclass` version is barely longer than the `NamedTuple`, is mutable by default, and grows cleanly as fields are added. That's why it's the best default.

## Related reading

- [Avoid common class mistakes](avoid-common-class-mistakes.md) — especially the mutable-class-attribute bug that dataclasses sidestep.
- [Dataclass parameters](../reference/dataclass-parameters.md) — every decorator option in one place.
- [Type hints guide](../../type-hints/) — for `TypedDict` details.
