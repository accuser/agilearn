---
title: Iterators and generators
---

# Iterators and generators

Iteration is everywhere in Python. Every `for` loop, every `in` check, every list comprehension, every unpacking — all of them go through the iterator protocol. Generators are the ergonomic way to build your own iterators, and `itertools` is a standard-library toolkit for composing them.

Understanding these well unlocks a style of programming that's both concise and memory-efficient — you can process files that don't fit in memory, pipelines that transform millions of records, and data flows where computation happens only when a value is actually needed.

## Sections

- **[Learn](learn/)** — four notebooks: how iteration works under the hood, writing generator functions, generator expressions and `itertools`, and building custom iterator classes for the cases where generators don't fit.
- **[Recipes](recipes/)** — processing large files lazily, chaining and grouping iterables, combining generators, and the mistakes that lose you a debugging evening.
- **[Reference](reference/)** — the iterator protocol, generator syntax, and a compact `itertools` cheatsheet.
- **[Concepts](concepts/)** — essays on laziness and memory, and on iteration as an interface (the cultural thing that makes Python's ecosystem compose so well).

New to the topic? Start with [Learn → Iteration protocol](learn/01-iteration-protocol.ipynb). Here for a specific task? [Recipes](recipes/) is task-focused and [Reference](reference/) is for lookups.
