---
title: Recipes
---

# Recipes: Concurrency

Task-focused how-tos. If you know what you want to do but aren't sure how to build it, this is the section to skim.

## Recipes in this section

- **[Run blocking calls in a thread pool](run-blocking-calls-in-a-thread-pool.ipynb)** — take a slow, blocking function you call many times (downloads, queries, file reads) and run them concurrently with `ThreadPoolExecutor`, collecting results in order or as they finish, and handling per-task failures.
- **[Parallelise CPU work across processes](parallelise-cpu-work-across-processes.ipynb)** — push a CPU-bound function across all your cores with `ProcessPoolExecutor`, chunk the work to keep overhead down, and measure the speedup honestly.
- **[Run async tasks concurrently](run-async-tasks-concurrently.ipynb)** — fan out many awaitables with `gather` and `TaskGroup`, cap how many run at once with a `Semaphore`, and add timeouts so one slow task can't stall the batch.
- **[Avoid common concurrency mistakes](avoid-common-concurrency-mistakes.md)** — a catalogue of the gotchas: races on shared state, the missing `__main__` guard, blocking the event loop, deadlocks, swallowed exceptions, and the speed-ups that never materialise.
