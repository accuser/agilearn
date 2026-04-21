---
title: Classes and objects
---

# Classes and objects

Classes let you bundle data and behaviour together and give them a name. Python supports the full spectrum — from quick `@dataclass` records that replace a dict-with-a-shape, through Pythonic classes with custom dunders that feel like built-in types, to inheritance hierarchies when they genuinely help. This guide walks through the mechanics, the idioms that make classes feel native, and the judgement calls about when to reach for them at all.

## Start here

If classes are new to you, work through the [**Learn**](learn/) section in order — five short notebooks, around fifteen to twenty minutes each. Every code cell can be edited and run in place, directly on the page; no install required.

If you already know the basics and are looking for a specific technique, jump to the [**Recipes**](recipes/) section, or scan the [**Reference**](reference/) for the dunder catalogue and syntax lookups.

## What this guide covers

**[Learn](learn/)** — classes and `__init__`, dunder methods, data classes, inheritance and composition, class vs instance attributes and the `@property`/`@classmethod`/`@staticmethod` trio.

**[Recipes](recipes/)** — choosing between `@dataclass`, `NamedTuple`, and plain classes; validating attributes on assignment; making a class iterable or container-like; avoiding common class mistakes.

**[Reference](reference/)** — a dunder-methods catalogue grouped by role, `@dataclass` parameters, and the syntax for `property`/`classmethod`/`staticmethod`.

**[Concepts](concepts/)** — when to reach for classes rather than functions and dicts; composition over inheritance in practice.
