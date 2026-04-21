---
title: Type hints
---

# Type hints

Python is dynamically typed — the interpreter doesn't check your variable types. Type *hints* are annotations that describe the types you *intend* a function or variable to have, so a separate tool (a type-checker like `mypy` or `pyright`) can flag mismatches before the code runs. Your editor uses them too, for better autocomplete and inline warnings.

This guide takes type hints from "I've seen those `->` arrows in other people's code" to "I can type my own functions, data structures, and gradual-typing a legacy module".

## Sections

- **[Learn](learn/)** — four notebooks: why bother, basic annotations, generics over built-in collections, and the trickier bits (`Optional`, `Union`, `Literal`, `Callable`, `TypedDict`).
- **[Recipes](recipes/)** — typing a function signature, typing a data structure, handling `None` cleanly, and the mistakes that trip people up.
- **[Reference](reference/)** — the `typing` module, the built-in generic forms (`list[int]`, `dict[str, int]`, etc.), and a compact mypy cheatsheet.
- **[Concepts](concepts/)** — short essays on *when* type hints help and what gradual typing actually buys you.

If you're new to type hints, start with [Learn → Why type hints](learn/01-why-type-hints.ipynb). If you're here for a specific question, [Recipes](recipes/) is task-focused, [Reference](reference/) is for lookups.

## Python version note

This guide assumes **Python 3.10+**. Two features matter:

- The `X | Y` union syntax (`int | str`) and `X | None` for optionals work in 3.10+. Earlier versions need `Union[int, str]` and `Optional[X]` from the `typing` module.
- Built-in generics (`list[int]`, `dict[str, int]`) work in 3.9+. Before that you'd write `List[int]`, `Dict[str, int]` from `typing`.

Most UK university environments ship Python 3.10 or later. If you're stuck on older Python, the [`typing` reference page](reference/typing-module-reference.md) shows the older equivalents.
