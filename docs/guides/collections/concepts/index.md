---
title: Concepts
---

# Concepts: Collections

Short essays on the ideas behind the `collections` module. Read these once and keep coming back to them when you're deciding how to store something.

## Essays in this section

- **[Why specialised containers](why-specialised-containers.md)** — what `Counter`, `deque`, and the rest buy you over a plain `dict` or `list`: not just speed (though `list.pop(0)` really is slow), but code that says what it means.
- **[Choosing a container](choosing-a-container.md)** — a decision guide across the whole module and the built-ins: `Counter` versus a manual count, `defaultdict` versus `setdefault`, `deque` versus `list`, `namedtuple` versus `dict` versus dataclass.
