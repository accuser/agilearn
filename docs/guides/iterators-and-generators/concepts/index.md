---
title: Concepts
---

# Concepts: Iterators and generators

Short essays on the ideas behind iteration in Python. Read these once and keep coming back to them when you're deciding how to shape data-processing code.

## Essays in this section

- **[Laziness and memory](laziness-and-memory.md)** — why lazy evaluation matters, when it's worth the complexity, and the trade-offs against eager approaches.
- **[Iteration as an interface](iteration-as-an-interface.md)** — how the iterator protocol is really a *contract* that lets completely different types plug into the same tools (`for`, `sum`, list comprehensions, `itertools`), and why that makes Python's ecosystem compose so well.
