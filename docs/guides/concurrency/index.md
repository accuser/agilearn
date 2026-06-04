---
title: Concurrency
---

# Concurrency

Most programs spend their time waiting — for a network reply, a disk read, a database query — or grinding through a calculation that pins a CPU core. Concurrency is how you stop wasting that time: overlap the waiting, or spread the grinding across cores. Python gives you three tools for this, and the hardest part is rarely the syntax — it's knowing which tool fits the problem in front of you.

This guide takes the three tools in turn — threads, processes, and `async`/`await` — and grounds each in the kind of work it's actually good at. The thread that runs through all of it is one distinction: **I/O-bound** work (waiting) versus **CPU-bound** work (computing). Get that right and the choice of tool nearly makes itself.

## Sections

- **[Learn](learn/)** — four notebooks: the concurrency-versus-parallelism mental model and Python's three tools, threads and the `concurrent.futures` thread pool for I/O-bound work, processes for true CPU parallelism, and `async`/`await` for high-volume I/O.
- **[Recipes](recipes/)** — running blocking calls in a thread pool, parallelising CPU work across processes, running async tasks concurrently with bounded fan-out, and the mistakes that cause races, deadlocks, and silent no-ops.
- **[Reference](reference/)** — an `asyncio` cheatsheet, a `concurrent.futures` reference, and a `threading`/`multiprocessing` primitives reference.
- **[Concepts](concepts/)** — essays on the GIL (what it really does, and the free-threaded future) and on choosing a concurrency model from first principles.

!!! note "Running these examples"
    Threads and processes don't run inside the in-browser sandbox — those examples are written as you'd run them in a real `.py` file, so try them locally. The `async` examples do run in the browser, but in a notebook cell you `await main()` directly instead of calling `asyncio.run(main())`; both forms are shown where it matters.

New to the topic? Start with [Learn → Concurrency models](learn/01-concurrency-models.ipynb). Here for a specific task? [Recipes](recipes/) is task-focused and [Reference](reference/) is for lookups.
