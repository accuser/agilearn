---
title: Learn
---

# Learn: Concurrency

Four notebooks, in order. Each is self-contained, but they build on each other — the first sets up the decision framework that the next three each fill in for one of Python's three tools.

## Notebooks in this section

1. **[Concurrency models](01-concurrency-models.ipynb)** — concurrency versus parallelism, the I/O-bound versus CPU-bound distinction that drives every choice, and a one-paragraph tour of the GIL. Ends with a map: which of Python's three tools fits which kind of work.
2. **[Threads and futures](02-threads-and-futures.ipynb)** — `threading.Thread`, then the higher-level `concurrent.futures.ThreadPoolExecutor` you should actually reach for. `submit`, `map`, `as_completed`, collecting results and exceptions, and why shared mutable state needs a `Lock`.
3. **[Processes and parallelism](03-processes-and-parallelism.ipynb)** — `ProcessPoolExecutor` and `multiprocessing` for CPU-bound work that the GIL otherwise serialises. Pickling constraints, the `if __name__ == "__main__"` guard, and how to measure whether parallelism actually paid off.
4. **[Async and await](04-async-await.ipynb)** — coroutines, the event loop, `asyncio.run`, `gather`, and `TaskGroup`. How a single thread juggles thousands of waiting connections, plus cancellation, timeouts, and the cardinal rule: never block the loop.

After these, the [Recipes](../recipes/) cover task-focused applications and the [Reference](../reference/) has quick lookups for `asyncio`, `concurrent.futures`, and the threading/multiprocessing primitives.
