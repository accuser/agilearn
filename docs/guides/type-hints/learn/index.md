---
title: Learn
---

# Learn: Type hints

Four notebooks, in order. Each is self-contained but they build on each other — if you work through them in sequence you'll cover the whole topic once.

## Notebooks in this section

1. **[Why type hints?](01-why-type-hints.ipynb)** — what they are, what they *aren't*, and what problem they solve. How type-checkers use them.
2. **[Basic annotations](02-basic-annotations.ipynb)** — annotating variables, function parameters, and return types. The built-in types (`int`, `str`, `bool`, etc.) and how they compose.
3. **[Generics and collections](03-generics-and-collections.ipynb)** — typing containers: `list[int]`, `dict[str, int]`, `tuple[int, str]`, custom generics via `TypeVar`.
4. **[Optional, Union, and friends](04-typing-special-forms.ipynb)** — `X | None`, `X | Y`, `Literal`, `Callable`, `TypedDict`, `Any` and `object`. The expressive forms you'll reach for as your typing gets more ambitious.

After these, the [Recipes](../recipes/) show task-focused applications and the [Reference](../reference/) has lookup tables for the `typing` module.
