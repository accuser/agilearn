---
title: Avoid common typing mistakes
---

# Avoid common typing mistakes

A catalogue of the traps that catch people when they start adding type hints, and the shape of the fix for each.

## `list` vs `List`

On Python 3.9+, prefer the built-in forms over the capitalised imports from `typing`:

```python
# Modern
scores: list[int] = []
ages: dict[str, int] = {}

# Legacy — still works but no longer needed
from typing import List, Dict
scores: List[int] = []
ages: Dict[str, int] = {}
```

The capitalised forms are deprecated but still supported for backwards compatibility. If you're writing new code for 3.9+, use the lowercase built-ins.

## Annotating with `list` instead of `list[int]`

```python
def process(items: list) -> int:     # accepts list of *anything*
    return sum(items)                # hopes for the best
```

`list` by itself means `list[Any]`. The type-checker can't help you — you've asked it not to. Write `list[int]` (or `Iterable[int]`) and the checker will catch callers passing the wrong thing.

Same trap with `dict`, `set`, `tuple` — always parameterise.

## Mutable default arguments

The classic Python footgun is unrelated to type hints but compounded by them:

```python
def add_tag(item: dict, tags: list[str] = []) -> dict:
    tags.append("new")    # mutates the shared default!
    item["tags"] = tags
    return item
```

The `[]` is evaluated once, at function definition. Every call that doesn't pass `tags` shares the same list. Fix: default to `None`, create inside.

```python
def add_tag(item: dict, tags: list[str] | None = None) -> dict:
    if tags is None:
        tags = []
    tags.append("new")
    item["tags"] = tags
    return item
```

The [functions guide](../../functions/recipes/use-default-and-keyword-arguments.ipynb) has more on this.

## `Optional[X]` doesn't mean "has a default"

```python
def greet(name: Optional[str]) -> str:
    return f"Hi, {name}"

greet()    # TypeError: missing required argument
```

`Optional[X]` means `X | None` — the argument can be `None`, but it's still required. For "has a default", give it a default:

```python
def greet(name: str | None = None) -> str:
    ...
```

## Forward references — `"ClassName"` as a string

When a class refers to itself (or two classes refer to each other), you can't use the class in its own annotation because the name isn't defined yet. Wrap the name in quotes — a "forward reference":

```python
class Node:
    def __init__(self, value: int, next: "Node | None" = None):
        self.value = value
        self.next = next
```

Better: `from __future__ import annotations` at the top of the file, which makes *all* annotations lazy-evaluated and lets you drop the quotes.

```python
from __future__ import annotations

class Node:
    def __init__(self, value: int, next: Node | None = None):
        ...
```

## Mutable collection parameters

```python
def sum_ages(people: list[dict]) -> int:
    return sum(p["age"] for p in people)
```

`list[dict]` requires callers to pass a `list`. If you just need to iterate, `Iterable[dict]` is more flexible:

```python
from collections.abc import Iterable

def sum_ages(people: Iterable[dict]) -> int:
    return sum(p["age"] for p in people)
```

Works with lists, tuples, sets, generators — anything iterable. Broader input types are usually better for library-ish code.

## Treating `bool` as `int` without thinking

`bool` is technically a subclass of `int` (`True == 1`, `False == 0`). Type-checkers allow `bool` where `int` is expected — so:

```python
def multiply(a: int, b: int) -> int:
    return a * b

multiply(3, True)    # type-checks, returns 3
```

This is rarely what you want. If your function shouldn't accept booleans, use a `Literal[...]` or a `TypeVar` with `bound=int` and `constraint`.

## Over-using `Any`

Every `Any` is a place where type errors slip through silently. Common misuse:

```python
def process(data: Any) -> Any:      # no type-checking at all
    return transform(data)
```

Alternatives:
- If you really mean "any Python object", use `object` — still no operations, but narrowing via `isinstance` works.
- If you mean "matches whatever the caller passes and preserves through", use `TypeVar`.
- If you mean "matches a known set of types", use a `Union` or `Literal`.

`Any` is an escape hatch, not a default.

## Generic `Callable[..., T]` everywhere

```python
def with_logging(fn: Callable[..., Any]) -> Callable[..., Any]:
    ...
```

The `...` loses all type information about the function. For simple decorators, use `ParamSpec` to preserve the wrapped function's signature:

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

def with_logging(fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper
```

`ParamSpec` (Python 3.10+) captures the whole parameter list so callers keep full typing.

## Misusing `cast`

`typing.cast(T, x)` tells the type-checker "trust me, this is a `T`" without any runtime check. Use it when you genuinely know more than the checker — e.g. after a database query that the checker can't see into. Don't use it as a way to silence a type error you don't understand.

```python
from typing import cast

# OK: you know this field is an int but the API returns a dict[str, Any]
user_id = cast(int, response["user_id"])

# NOT OK: the checker is warning you for a reason
x: str = cast(str, 42)   # lies to the checker; will explode at runtime
```

## Variance gotchas

`list[Animal]` is NOT a supertype of `list[Dog]`, even though `Dog` is a subtype of `Animal`. This is because `list` is mutable — if `list[Dog]` were treated as `list[Animal]`, you could append a `Cat` to it through the Animal view, breaking the Dog-only invariant.

For read-only use, `Sequence[Animal]` accepts `Sequence[Dog]` — the abstract types are variance-friendly. This is why it's usually a good idea to accept the abstract container types for parameters.

## Circular imports for type-only usage

If you need to reference a type only in annotations (never actually call it), and importing it would create a circular import, guard the import:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User     # only evaluated by type-checkers

def save(user: "User") -> None:
    ...
```

`TYPE_CHECKING` is `False` at runtime, so the import doesn't actually happen. You need the forward-reference quotes (or `from __future__ import annotations`) for the annotation.
