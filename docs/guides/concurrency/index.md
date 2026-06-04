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
    Cells that need real threads or processes can't run in the in-browser runtime, so they have **no Run button** and are marked *"runs locally only"* — they're written as complete `.py` scripts, so copy them into your own editor to try them. The `async` examples *do* run here; in a notebook cell you `await main()` directly instead of calling `asyncio.run(main())`, and both forms are shown where it matters.

New to the topic? Start with [Learn → Concurrency models](learn/01-concurrency-models.ipynb). Here for a specific task? [Recipes](recipes/) is task-focused and [Reference](reference/) is for lookups.
