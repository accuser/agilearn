---
title: Recipes
---

# Recipes: Type hints

Task-focused how-tos. If you know what you want to do but aren't sure how to type it, this is the section to skim.

## Recipes in this section

- **[Type a function signature](type-a-function-signature.ipynb)** — parameters, defaults, variadic args (`*args`, `**kwargs`), return types, and how to document what a function actually takes.
- **[Type a data structure](type-a-data-structure.ipynb)** — when to use `TypedDict`, when to use a dataclass, when `NamedTuple` fits, and when a plain `dict[str, int]` is enough.
- **[Work with `Optional` values](work-with-optional-values.ipynb)** — the `X | None` pattern, narrowing with `if x is not None`, and why `Optional[X]` doesn't mean "this argument has a default".
- **[Avoid common typing mistakes](avoid-common-typing-mistakes.md)** — a short catalogue of the traps: `list` vs `List`, mutable defaults, forward references, variance gotchas.
