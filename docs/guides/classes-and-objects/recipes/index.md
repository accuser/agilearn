---
title: Recipes
---

# Recipes: Classes and objects

Short, task-focused how-tos for specific things you'll want to do when working with classes. Each recipe assumes you already know the basics — if a term surprises you, the [Learn](../learn/) section is one click away.

Unlike the tutorials, the recipes don't have a recommended order. Pick whichever is useful right now.

## Recipes in this guide

- **[Choose between `@dataclass`, `NamedTuple`, and a plain class](choose-between-dataclass-namedtuple-class.md)** — a decision guide for the three ways to define a record-like type.
- **[Validate attributes on assignment](validate-attributes-on-assignment.ipynb)** — using `__post_init__` and `@property` setters to enforce invariants.
- **[Make a class iterable or container-like](make-a-class-iterable.ipynb)** — implementing `__iter__`, `__getitem__`, `__len__`, and `__contains__`.
- **[Avoid common class mistakes](avoid-common-class-mistakes.md)** — mutable class attributes, deep inheritance, `super()` ordering, and other traps.
