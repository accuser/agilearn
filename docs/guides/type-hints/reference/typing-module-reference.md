---
title: typing module reference
---

# `typing` module reference

The core forms you'll reach for, with the Python version each first arrived in. The legacy `typing` imports for built-in collections (`List`, `Dict`, etc.) are covered in the [built-in generics reference](built-in-generic-types.md).

## Unions and optionals

| Form | Since | Meaning |
| --- | --- | --- |
| `X \| Y` | 3.10 | Union of two types |
| `Union[X, Y]` | 3.5 | Same as `X \| Y`, legacy spelling |
| `X \| None` | 3.10 | Optional — `X` or `None` |
| `Optional[X]` | 3.5 | Same as `X \| None` |

Prefer the `|` syntax on 3.10+. `Optional[X]` is still accepted and still readable — don't rewrite working code for the sake of it.

## Specific-value types

| Form | Since | Meaning |
| --- | --- | --- |
| `Literal["a", "b"]` | 3.8 | Must be exactly one of those literal values |
| `LiteralString` | 3.11 | Any string whose value is statically known |

`Literal` works for `str`, `int`, `bool`, `bytes`, `None`, and enum members.

## Callables

| Form | Since | Meaning |
| --- | --- | --- |
| `Callable[[A, B], R]` | 3.5 | Callable taking `A, B`, returning `R` |
| `Callable[..., R]` | 3.5 | Callable taking any args, returning `R` |
| `Callable[P, R]` | 3.10 | Callable with param-spec `P` (see `ParamSpec`) |

From 3.9+, prefer `collections.abc.Callable` over `typing.Callable`.

## Generics

| Form | Since | Meaning |
| --- | --- | --- |
| `TypeVar("T")` | 3.5 | Generic type parameter |
| `TypeVar("T", bound=X)` | 3.5 | `T` is a subtype of `X` |
| `TypeVar("T", X, Y)` | 3.5 | `T` is one of `X` or `Y` (constraint set) |
| `Generic[T]` | 3.5 | Class-level generic — `class Stack(Generic[T]):` |
| `ParamSpec("P")` | 3.10 | Captures a parameter list (for decorators) |
| `TypeVarTuple("Ts")` | 3.11 | Variadic generic over tuples |
| `type parameters in signatures` | 3.12 | `def first[T](xs: Sequence[T]) -> T:` — no `TypeVar` needed |

## Structured forms

| Form | Since | Meaning |
| --- | --- | --- |
| `TypedDict` | 3.8 | Dict with typed string keys |
| `NamedTuple` | 3.6 (typing form), 3.5 (collections) | Tuple with named fields |
| `Protocol` | 3.8 | Structural typing — "anything with these methods" |
| `NotRequired[X]` | 3.11 | A `TypedDict` field that may be absent |
| `Required[X]` | 3.11 | A `TypedDict` field that must be present |

## Escape hatches and special forms

| Form | Since | Meaning |
| --- | --- | --- |
| `Any` | 3.5 | Disables type-checking for this position |
| `object` | always | Any Python object — still checked |
| `Never` | 3.11 | A value that can never be produced (bottom type) |
| `NoReturn` | 3.5 | Return annotation for functions that never return |
| `Self` | 3.11 | The current class — for method return types |

## Advanced

| Form | Since | Meaning |
| --- | --- | --- |
| `Final[X]` | 3.8 | Cannot be reassigned |
| `ClassVar[X]` | 3.5 | Class-level attribute (not instance) |
| `NewType("UserId", int)` | 3.5 | Distinct type from `int` at check-time |
| `TypeAlias` | 3.10 | Explicit type-alias declaration |
| `Annotated[X, ...]` | 3.9 | Attach metadata to a type (for runtime use) |
| `cast(X, value)` | 3.5 | Tell the checker "trust me this is an X" |

## Inspection

| Function | What it does |
| --- | --- |
| `get_type_hints(obj)` | Returns the annotations dict with forward refs resolved |
| `get_args(T)` | Returns the type arguments — `get_args(list[int])` is `(int,)` |
| `get_origin(T)` | Returns the unparameterised form — `get_origin(list[int])` is `list` |

## Deprecated (but still working)

The `typing.List`, `typing.Dict`, `typing.Tuple`, `typing.Set`, `typing.FrozenSet`, `typing.Type` forms still work but are deprecated in favour of the built-ins (`list`, `dict`, `tuple`, `set`, `frozenset`, `type`) from 3.9+.

## Version compatibility table

If you're targeting multiple Python versions:

| Feature | 3.8 | 3.9 | 3.10 | 3.11 | 3.12 |
| --- | --- | --- | --- | --- | --- |
| `list[int]` etc. | `List[int]` | ✔ | ✔ | ✔ | ✔ |
| `X \| Y` | `Union[X, Y]` | `Union[X, Y]` | ✔ | ✔ | ✔ |
| `X \| None` | `Optional[X]` | `Optional[X]` | ✔ | ✔ | ✔ |
| `ParamSpec` | `typing_extensions` | `typing_extensions` | ✔ | ✔ | ✔ |
| `NotRequired` | `typing_extensions` | `typing_extensions` | `typing_extensions` | ✔ | ✔ |
| `Self` | `typing_extensions` | `typing_extensions` | `typing_extensions` | ✔ | ✔ |
| `type params in signatures` | — | — | — | — | ✔ |

The `typing_extensions` package is the backport — `from typing_extensions import NotRequired` works on any version.
