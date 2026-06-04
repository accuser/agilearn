---
title: Concepts
---

# Concepts: Concurrency

Short essays on the ideas behind concurrency in Python. Read these once and keep coming back to them when you're deciding how to shape work that waits or work that computes.

## Essays in this section

- **[The GIL and what it means](the-gil-and-what-it-means.md)** — the Global Interpreter Lock: why it exists, what it actually prevents (and what it doesn't), why it makes threads useless for CPU-bound work but fine for I/O, and what the free-threaded builds of Python 3.13+ change.
- **[Choosing a concurrency model](choosing-a-concurrency-model.md)** — a first-principles walk from "what is my program waiting on?" to a confident choice between threads, processes, and `async`. The distinctions that matter and the questions to ask before you reach for any of them.
