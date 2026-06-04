---
title: The GIL and what it means
---

# The GIL and what it means

Few three-letter acronyms generate as much folklore as Python's GIL. It's blamed for things it doesn't cause and credited with things it doesn't do. This essay is the version worth carrying around: what the Global Interpreter Lock actually is, the one rule it imposes, and how that single rule explains why threads are brilliant for some work and useless for other work.

## What it is

The **Global Interpreter Lock** is a mutex inside CPython — the standard Python interpreter — that allows **only one thread to execute Python bytecode at a time**. Not one thread per object, not one thread per module: one thread, full stop, across the whole interpreter. A thread must hold the GIL to run Python code, and it releases it periodically so others get a turn.

That's the entire mechanism. Everything else about the GIL is a consequence of this one sentence.

## Why it exists

CPython manages memory by **reference counting**: every object keeps a tally of how many things point at it, and is freed when the tally hits zero. Those counts are updated constantly — every assignment, every function call, every loop iteration nudges them. If two threads adjusted the same count at the same instant, the count could corrupt: objects freed while still in use, or never freed at all.

The GIL is the blunt, cheap fix. By guaranteeing that only one thread touches interpreter internals at once, reference counting stays correct without a lock on every single object. That keeps single-threaded Python — which is most Python — fast and simple, and it makes integrating C libraries far easier. The GIL is not an oversight; it's a deliberate trade that favoured the common case. The cost lands squarely on multi-threaded computation.

## The one rule, and its consequence

The rule: **one thread runs Python bytecode at a time.** The consequence: threads can't speed up *computation*. Spin up eight threads to crunch numbers on an eight-core machine and they'll politely take turns on what amounts to a single core, plus overhead — often *slower* than not threading at all.

If that were the whole story, threads would be pointless. But there's a critical exception built into the rule.

## The exception that makes threads useful

A thread **releases the GIL while it waits.** When a thread makes a blocking I/O call — reading a socket, querying a database, waiting on a disk — it lets go of the lock, because it's not running Python bytecode during the wait; it's parked. Another thread immediately picks up the GIL and runs. Many well-written C extensions release it too, around heavy work that doesn't touch Python objects.

This is why the I/O-bound versus CPU-bound distinction is *the* distinction:

- **I/O-bound work** is mostly waiting, and threads release the GIL while waiting. So a hundred threads can all be blocked on a hundred sockets simultaneously — the waits overlap, and throughput soars. Threads work beautifully here.
- **CPU-bound work** never waits; it holds the GIL the whole time. Threads can only take turns, so there's no gain. This work needs processes.

Hold those two sentences and you can predict whether threading will help before writing a line.

## Processes: the way around

Because the GIL is *per interpreter*, the way to get genuine parallel computation is to run **more interpreters** — that is, more processes. Each process has its own GIL, its own memory, its own reference counts, and runs on its own core. Eight processes on eight cores give roughly eightfold computation, minus the cost of starting them and shipping data across the process boundary by `pickle`.

The price of dodging the GIL this way is that processes don't share memory. Data must be copied in and out, which is why process-based parallelism rewards coarse-grained work (big chunks, infrequent handoffs) and punishes fine-grained chatter.

## What the GIL is *not*

A few corrections worth internalising:

- **It is not a Python-the-language feature.** It's a CPython implementation detail. Jython and IronPython have no GIL; they solve memory safety differently.
- **It does not make threads safe.** Race conditions are alive and well — the GIL can release between any two bytecodes, so `x += 1` from two threads can still lose updates. You still need locks for shared mutable state.
- **It does not affect `async`.** Asyncio runs everything on one thread by design, so the GIL is simply irrelevant to it.
- **It does not cap I/O concurrency.** Threads waiting on I/O release it, so the GIL is no obstacle to thousands of concurrent connections.

## The free-threaded future

For most of Python's history the GIL was simply a fact of life. That is now changing. **PEP 703** introduced an officially supported **free-threaded** build of CPython, available experimentally from **Python 3.13**, that removes the GIL entirely and lets threads run Python bytecode in genuine parallel.

It's not a free lunch. Removing the GIL requires finer-grained locking inside the interpreter, which can slow single-threaded code, and the wider ecosystem of C extensions needs time to adapt and be made thread-safe. For now it's an opt-in build, running alongside the standard one rather than replacing it. But the direction is set: over the coming years, "use processes for CPU-bound work" may soften from an iron rule to a default you sometimes override.

Until free-threading is the norm, the mental model in this guide holds. Know what your program is waiting on, remember that threads release the GIL while they wait, and the choice between threads and processes follows directly. The next essay, [choosing a concurrency model](choosing-a-concurrency-model.md), turns that into a decision you can make quickly.
