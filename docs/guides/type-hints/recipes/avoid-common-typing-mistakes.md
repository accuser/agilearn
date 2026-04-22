# Avoid common typing mistakes

**The question.** You're adding types to existing Python code, and the type-checker is either too quiet (silent `Any` everywhere) or too loud (mysterious variance complaints). You want the shortlist of traps and the shape of the fix for each.

Below is the summary, then each trap in detail.

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `from typing import List` on 3.9+ | Deprecated capitalised form | `list[int]`, `dict[str, int]`, etc. |
| `items: list` (no parameter) | Same as `list[Any]` — no checking | `list[int]` or `Iterable[int]` |
| `tags: list = []` | Shared mutable default across calls | `tags: list \| None = None`, construct inside |
| `name: Optional[str]` (no default) | Argument is still required | `name: str \| None = None` for "has a default" |
| `next: Node` inside `class Node:` | `Node` not defined yet | `next: 'Node \| None' = None` or `from __future__ import annotations` |
| `people: list[dict]` when you only iterate | Over-restrictive parameter | `Iterable[dict]` |
| `def f(a: int): ...; f(True)` | `bool` is an `int` — passes the check | `Literal[0, 1]` or explicit validation |
| `data: Any` | Turns off type-checking | `object`, a `TypeVar`, or a union |
| `Callable[..., Any]` on a decorator | Loses the wrapped function's types | `Callable[P, R]` with `ParamSpec` |
| `cast(int, response['x'])` to silence an error | Lies to the checker | Only cast when you genuinely know more than it does |
| `list[Dog]` used as `list[Animal]` | Mutable containers are invariant | Use `Sequence[Animal]` for read-only use |
| Type-only import causing a cycle | Real runtime import, real cycle | `if TYPE_CHECKING: from ... import ...` |

Each of these in turn below.

## `list` vs `List`

On Python 3.9+, prefer the built-in lowercase forms:

```python
# Modern
scores: list[int] = []
ages:   dict[str, int] = {}

# Legacy — still works but no longer needed
from typing import List, Dict
scores: List[int] = []
```

The capitalised forms are deprecated but still supported. For new code on 3.9+, use the lowercase built-ins.

## Annotating with `list` instead of `list[int]`

```python
def process(items: list) -> int:     # accepts list of ANYTHING
    return sum(items)                # hopes for the best
```

`list` by itself is `list[Any]`. The checker can't help — you've asked it not to. Write `list[int]` (or `Iterable[int]` if you only iterate) and the checker will flag callers that pass the wrong thing. Same trap with `dict`, `set`, `tuple` — always parameterise.

## Mutable default arguments

```python
def add_tag(item: dict, tags: list[str] = []) -> dict:
    tags.append('new')    # mutates the SHARED default!
    item['tags'] = tags
    return item
```

The `[]` is evaluated once, at function definition. Every call that doesn't pass `tags` shares the same list. Fix: default to `None`, construct inside.

```python
def add_tag(item: dict, tags: list[str] | None = None) -> dict:
    if tags is None:
        tags = []
    ...
```

## `Optional[X]` doesn't mean "has a default"

```python
def greet(name: Optional[str]) -> str:
    return f'Hi, {name}'

greet()    # TypeError: missing required argument
```

`Optional[X]` means `X | None` — the argument *can* be `None`, but it's still required. To also give it a default, provide one:

```python
def greet(name: str | None = None) -> str:
    ...
```

## Forward references

When a class refers to itself (or two classes refer to each other), you can't use the class in its own annotation because the name isn't defined yet. Wrap in quotes:

```python
class Node:
    def __init__(self, value: int, next: 'Node | None' = None):
        self.value = value
        self.next = next
```

Better: `from __future__ import annotations` at the top makes **all** annotations lazy-evaluated and lets you drop the quotes.

## Mutable collection parameters

```python
def sum_ages(people: list[dict]) -> int:
    return sum(p['age'] for p in people)
```

`list[dict]` forces callers to pass a list. If you just iterate, `Iterable[dict]` is more flexible — works with lists, tuples, sets, generators. Broader input types are usually better for library code.

## Treating `bool` as `int` without thinking

`bool` is a subclass of `int` (`True == 1`, `False == 0`), so `multiply(3, True)` type-checks. Usually not what you want; use `Literal[0, 1]` or explicit validation if you need to reject booleans.

## Over-using `Any`

Every `Any` is a place where type errors slip through silently.

```python
def process(data: Any) -> Any:      # no type-checking at all
    return transform(data)
```

Alternatives:

- If you mean "any Python object", use `object` — still no operations, but `isinstance` narrowing works.
- If you mean "matches whatever the caller passes, preserved through", use `TypeVar`.
- If you mean "a known set of types", use a union or `Literal`.

`Any` is an escape hatch, not a default.

## Generic `Callable[..., T]` on a decorator

```python
def with_logging(fn: Callable[..., Any]) -> Callable[..., Any]:
    ...
```

The `...` loses all type information about the function. For decorators, use `ParamSpec` to preserve the wrapped signature:

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable

P = ParamSpec('P')
R = TypeVar('R')

def with_logging(fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f'calling {fn.__name__}')
        return fn(*args, **kwargs)
    return wrapper
```

`ParamSpec` (Python 3.10+) captures the whole parameter list so callers keep full typing.

## Misusing `cast`

`typing.cast(T, x)` tells the checker "trust me, this is a `T`" with no runtime check. Use it when you genuinely know more than the checker (e.g. after a database fetch it can't see into); don't use it to silence a warning you don't understand.

```python
# OK: the field really is an int, but response is dict[str, Any]
user_id = cast(int, response['user_id'])

# NOT OK: lies to the checker, explodes at runtime
x: str = cast(str, 42)
```

## Variance gotchas

`list[Animal]` is **not** a supertype of `list[Dog]`, even though `Dog` is a subtype of `Animal`. Because `list` is mutable, treating `list[Dog]` as `list[Animal]` would let you append a `Cat` through the Animal view — breaking the Dog invariant.

For read-only use, `Sequence[Animal]` accepts `Sequence[Dog]` — the abstract types are variance-friendly. This is why accepting abstract container types for parameters is often the right move.

## Circular imports for type-only usage

If you need a type only in annotations (never actually call it), and importing would create a circular import, guard the import:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User     # only evaluated by type-checkers

def save(user: 'User') -> None:
    ...
```

`TYPE_CHECKING` is `False` at runtime, so the import doesn't happen. Pair with forward-reference quotes or `from __future__ import annotations`.

## When the shortcut is fine

Bare `list`, `dict`, `Any`, and `Callable[..., T]` all have their place — prototyping, dynamic data, edges of a system where types genuinely can't be pinned down. The traps bite when those escapes appear in the middle of otherwise-typed code, where the checker was *trying* to help and was told to stop.

When in doubt, type every parameter and every return in your public API. The internal helpers can be less rigorous; the public surface is the contract.

## Related reading

- [Type a function signature](type-a-function-signature.ipynb) — the canonical shape before the traps start.
- [Work with optional values](work-with-optional-values.ipynb) — the `X | None` patterns in more detail.
- [mypy cheatsheet](../reference/mypy-cheatsheet.md) — getting `mypy` actually running, with the flags you'll most often want.
