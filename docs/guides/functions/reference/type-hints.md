# Type hint syntax

This reference covers the syntax for adding type annotations to Python functions. Type hints do not enforce types at runtime. They serve as documentation, enable static analysis tools such as `mypy`, and improve editor support.

## Basic type annotations

Annotate parameters with a colon and the return value with `->`.

```python
def add(a: int, b: int) -> int:
    return a + b
```

### Primitive types

| Annotation | Python type | Example values |
|------------|------------|----------------|
| `int` | Integer | `0`, `42`, `-7` |
| `float` | Floating-point number | `3.14`, `-0.5` |
| `str` | String | `"hello"`, `""` |
| `bool` | Boolean | `True`, `False` |
| `bytes` | Byte sequence | `b"data"` |
| `None` | The `None` singleton | `None` |

```python
def is_positive(n: float) -> bool:
    return n > 0

def to_bytes(text: str) -> bytes:
    return text.encode("utf-8")

def do_nothing() -> None:
    pass
```

## Collection types

Since Python 3.9, built-in collection types can be used directly in annotations. For earlier versions, import the capitalised forms from the `typing` module.

| Annotation (3.9+) | `typing` equivalent (3.8 and earlier) | Description |
|--------------------|--------------------------------------|-------------|
| `list[int]` | `List[int]` | A list of integers |
| `dict[str, int]` | `Dict[str, int]` | A dictionary mapping strings to integers |
| `tuple[str, int]` | `Tuple[str, int]` | A tuple with exactly one string and one integer |
| `tuple[int, ...]` | `Tuple[int, ...]` | A tuple of arbitrary length containing integers |
| `set[str]` | `Set[str]` | A set of strings |
| `frozenset[int]` | `FrozenSet[int]` | A frozenset of integers |

### Examples

```python
def total(values: list[int]) -> int:
    return sum(values)

def word_count(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

def first_and_last(items: list[str]) -> tuple[str, str]:
    return items[0], items[-1]
```

### Nested collections

```python
def group_by_initial(names: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for name in names:
        key = name[0].upper()
        groups.setdefault(key, []).append(name)
    return groups
```

## Union types

Use union types when a value can be one of several types.

### `X | Y` syntax (Python 3.10+)

```python
def double(value: int | float) -> int | float:
    return value * 2
```

### `Union[X, Y]` (Python 3.9 and earlier)

```python
from typing import Union

def double(value: Union[int, float]) -> Union[int, float]:
    return value * 2
```

## Optional types

An optional type indicates that a value can be of a given type or `None`.

### `X | None` syntax (Python 3.10+)

```python
def find_user(user_id: int) -> str | None:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)
```

### `Optional[X]` (Python 3.9 and earlier)

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)
```

`Optional[X]` is equivalent to `Union[X, None]`.

## The `Any` type

`Any` indicates that a value can be of any type. Static type checkers will not flag operations on `Any` values.

```python
from typing import Any

def log(message: Any) -> None:
    print(str(message))
```

Use `Any` sparingly. It effectively disables type checking for that value.

## The `Callable` type

Use `Callable` to annotate parameters or return values that are functions.

```python
from collections.abc import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

apply(lambda x, y: x + y, 3, 5)  # 8
```

The syntax is `Callable[[parameter_types], return_type]`.

| Pattern | Meaning |
|---------|---------|
| `Callable[[int], str]` | A function taking one `int` parameter, returning `str` |
| `Callable[[int, int], bool]` | A function taking two `int` parameters, returning `bool` |
| `Callable[..., int]` | A function with any parameters, returning `int` |
| `Callable[[], None]` | A function taking no parameters, returning `None` |

For Python 3.8, import from `typing` instead of `collections.abc`.

## `TypeVar` for generic functions

`TypeVar` defines a type variable, allowing you to write functions that work with any type while preserving type relationships.

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

first([1, 2, 3])        # Type checker infers int
first(["a", "b", "c"])  # Type checker infers str
```

### Constrained type variables

```python
from typing import TypeVar

Number = TypeVar("Number", int, float)

def add(a: Number, b: Number) -> Number:
    return a + b
```

### Bound type variables

```python
from typing import TypeVar

T = TypeVar("T", bound=float)

def largest(a: T, b: T) -> T:
    return a if a >= b else b
```

## The `Literal` type

`Literal` restricts a value to specific literal values (Python 3.8 and later).

```python
from typing import Literal

def set_direction(direction: Literal["north", "south", "east", "west"]) -> None:
    print(f"Heading {direction}")

set_direction("north")   # Valid
# set_direction("up")    # Type checker error
```

## Return type annotations

### Common return type patterns

| Pattern | Meaning |
|---------|---------|
| `-> int` | Returns an integer |
| `-> None` | Returns nothing (or returns `None` explicitly) |
| `-> str \| None` | Returns a string or `None` |
| `-> tuple[int, str]` | Returns a tuple of an integer and a string |
| `-> list[dict[str, int]]` | Returns a list of dictionaries |
| `-> "ClassName"` | Forward reference to a class not yet defined |

### Forward references

When a type is not yet defined at the point of annotation, use a string literal.

```python
class Node:
    def next(self) -> "Node | None":
        pass
```

From Python 3.11 onwards, `from __future__ import annotations` makes all annotations strings by default, removing the need for manual quoting.

## Variable annotations

Variables can also carry type annotations, independent of function signatures.

```python
name: str = "Alice"
age: int = 30
scores: list[int] = []
config: dict[str, str | int] = {}
```

Variable annotations without assignment are also valid. They serve as declarations.

```python
result: int  # Declares the type without assigning a value
```

## The `TYPE_CHECKING` constant

`TYPE_CHECKING` is `False` at runtime but `True` when a static type checker analyses the code. Use it to avoid circular imports or expensive imports that are only needed for annotations.

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heavy_module import HeavyClass

def process(obj: HeavyClass) -> None:
    pass
```

## Python version compatibility

| Feature | Minimum Python version |
|---------|----------------------|
| Basic annotations (`int`, `str`) | 3.0 |
| `typing` module | 3.5 |
| `Literal` | 3.8 |
| Built-in generics (`list[int]`) | 3.9 |
| `X \| Y` union syntax | 3.10 |
| `Self` type | 3.11 |
| `type` statement for type aliases | 3.12 |

## Quick reference of common patterns

| What you want to express | Annotation |
|--------------------------|------------|
| An integer parameter | `x: int` |
| A string return value | `-> str` |
| A list of floats | `list[float]` |
| A dictionary from strings to integers | `dict[str, int]` |
| A value that could be a string or `None` | `str \| None` |
| A function that takes an `int` and returns a `str` | `Callable[[int], str]` |
| Any type at all | `Any` |
| One of specific literal values | `Literal["a", "b", "c"]` |
| A generic type variable | `T = TypeVar("T")` |
| A fixed-length tuple | `tuple[int, str, float]` |
| A variable-length tuple of one type | `tuple[int, ...]` |
| No return value | `-> None` |
