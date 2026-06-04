---
title: Choosing a concurrency model
---

# Choosing a concurrency model

Python gives you three concurrency tools, and most of the difficulty people have with the topic isn't writing threads or coroutines — it's not knowing which of the three to reach for. The good news is that the choice is far more systematic than it looks. A handful of questions, asked in the right order, lead almost mechanically to the right tool. This essay lays out those questions and the reasoning under them.

## First, a question that isn't about tools

Before *which* concurrency, ask **whether**. Concurrency adds real cost: races, deadlocks, harder debugging, code that's correct on your laptop and wrong under load. If a program is fast enough run plainly, adding concurrency only adds ways for it to break. The honest first answer is often "none — it's quick already."

Concurrency earns its complexity when there's a *measured* problem: a batch that takes minutes of mostly waiting, a computation that pins one core while seven idle, a server that must hold thousands of connections open. Reach for it then, not by default.

## The question that decides almost everything

If you do need it, one distinction does most of the work:

> **Is the program waiting, or computing?**

- It's **I/O-bound** if it spends its time *waiting* on something external — a network reply, a disk, a database, a user. The CPU is idle during the wait.
- It's **CPU-bound** if it spends its time *computing* — parsing, hashing, crunching, transforming. The CPU is busy throughout.

This isn't a stylistic preference; it's a property of the work, and it points at the tool directly. The reason traces back to the GIL (covered in [its own essay](the-gil-and-what-it-means.md)): Python threads can overlap *waiting* but not *computing*, because only one thread runs Python at a time. So:

- **CPU-bound → processes.** Only separate processes give you more than one core's worth of Python. Threads and async cannot speed up computation; don't waste effort trying.
- **I/O-bound → threads or async.** Both overlap waiting. Which one is a second question.

If a workload is genuinely both — say, download a thousand files (I/O) then compress them (CPU) — split it: async or threads for the fetching, a process pool for the compressing. Treating a mixed pipeline as one thing is a common source of "why didn't this get faster?"

## Splitting I/O-bound: threads versus async

Both threads and `asyncio` handle waiting well, so the choice between them is about *scale*, *style*, and *what you're calling*.

**Threads (`ThreadPoolExecutor`)** suit a few to a few hundred concurrent operations, especially when you're using ordinary **blocking** libraries — the synchronous database driver, `requests`, a file API. You don't have to rewrite anything; you wrap existing blocking calls in a pool and they overlap. The cost is that each thread carries OS overhead, so tens of thousands of them is impractical, and shared mutable state needs locking.

**`asyncio`** suits *high-volume* I/O — hundreds to many thousands of simultaneous connections — because all those tasks live on one thread as cheap coroutine objects, not OS threads. The cost is that it's all-in: a coroutine only yields at `await`, so **every** library in the hot path must be async-aware. One blocking call freezes the entire loop. You also pay in style — `async` colours your functions and propagates up through your call stack.

A useful way to decide: if your libraries are already async (or you're starting fresh and can choose async ones), and you need to hold many connections at once, choose `asyncio`. If you're adding concurrency to existing synchronous code, or the count is modest, threads are the lower-friction choice. When you're in async code but must call something blocking, you don't have to abandon the model — push it to a thread with `asyncio.to_thread`.

## The decision in one table

| What's true | Reach for | Because |
| --- | --- | --- |
| The work computes (parse, hash, crunch) | **Processes** (`ProcessPoolExecutor`) | only separate interpreters beat the GIL |
| The work waits; modest count; blocking libraries | **Threads** (`ThreadPoolExecutor`) | overlaps waits with no rewrite |
| The work waits; high volume; async-capable libraries | **`asyncio`** | thousands of tasks on one cheap thread |
| Mixed waiting and computing | **Both, split by stage** | each stage gets the right tool |
| It's already fast enough | **Nothing** | concurrency is cost without benefit |

## Three questions, in order

Boiled down, the whole decision is a short interrogation:

1. **Do I actually have a measured performance problem?** If no, stop.
2. **Is the slow part waiting or computing?** Computing → processes. Waiting → continue.
3. **How many waits at once, and are my libraries async?** Modest / blocking → threads. Many / async → `asyncio`.

That's it. The syntax of each tool is a day's learning; this judgement is what makes the syntax pay off. Get the I/O-versus-CPU call right and you'll rarely choose the wrong tool — and you'll understand *why* the few hard cases are hard. From here, the [Learn notebooks](../learn/index.md) build each tool out, and the [Reference](../reference/index.md) is there for the syntax once you know which page you need.
