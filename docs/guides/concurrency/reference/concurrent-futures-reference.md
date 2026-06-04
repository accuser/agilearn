---
title: concurrent.futures reference
---

# `concurrent.futures` reference

One high-level interface, two interchangeable engines. Use a **thread** pool for I/O-bound work and a **process** pool for CPU-bound work — the method names are identical.

```python
from concurrent.futures import (
    ThreadPoolExecutor, ProcessPoolExecutor,
    as_completed, wait, Future, TimeoutError,
)
```

## Creating an executor

| Constructor | For | Default workers |
| --- | --- | --- |
| `ThreadPoolExecutor(max_workers=None)` | I/O-bound | `min(32, os.cpu_count() + 4)` |
| `ProcessPoolExecutor(max_workers=None)` | CPU-bound | `os.cpu_count()` |

Always use as a context manager so workers are cleaned up:

```python
with ThreadPoolExecutor(max_workers=8) as pool:
    ...
# on exit: waits for running tasks, then shuts the pool down
```

## Submitting work

| Method | Returns | Order | Notes |
| --- | --- | --- | --- |
| `pool.submit(fn, *args, **kwargs)` | a single `Future` | — | starts immediately; most flexible |
| `pool.map(fn, iterable, timeout=None, chunksize=1)` | iterator of results | **input order** | re-raises the first exception on iteration |
| `pool.map(fn, it_a, it_b)` | results of `fn(a, b)` | input order | multiple iterables, like built-in `map` |

`chunksize` only matters for `ProcessPoolExecutor` — it batches inputs per worker to cut pickling overhead. It's ignored by thread pools.

```python
futures = [pool.submit(work, x) for x in items]   # submit form
results = list(pool.map(work, items))             # map form (ordered)
```

## The `Future` object

A handle to a result that may not exist yet.

| Method | Does |
| --- | --- |
| `future.result(timeout=None)` | block for the value; **re-raises** any exception from the worker |
| `future.exception(timeout=None)` | return the exception (or `None`) without raising |
| `future.done()` | `True` if finished, failed, or cancelled |
| `future.cancel()` | cancel if not yet started; returns whether it worked |
| `future.cancelled()` / `future.running()` | inspect state |
| `future.add_done_callback(fn)` | call `fn(future)` when it completes |

**You must retrieve results** — an exception sits silently on the future until `.result()` or `.exception()` is called.

## Collecting results

### In completion order — `as_completed`

```python
future_to_item = {pool.submit(work, x): x for x in items}
for future in as_completed(future_to_item):     # yields as each finishes
    item = future_to_item[future]
    try:
        result = future.result()
    except Exception as exc:
        handle(item, exc)
```

### Waiting on a set — `wait`

```python
done, not_done = wait(futures, timeout=10, return_when=ALL_COMPLETED)
# return_when: FIRST_COMPLETED | FIRST_EXCEPTION | ALL_COMPLETED
```

## Shutdown

| Call | Does |
| --- | --- |
| leaving the `with` block | waits for pending tasks, then shuts down |
| `pool.shutdown(wait=True)` | explicit equivalent |
| `pool.shutdown(wait=False, cancel_futures=True)` | cancel queued (not-yet-started) tasks (3.9+) |

## Process-pool caveats

- The worker function and its arguments/results must be **picklable** — no lambdas or locally defined functions.
- Launch must sit under `if __name__ == "__main__":`.
- Large arguments and return values are **copied** between processes; keep them lean.

See the [processes notebook](../learn/03-processes-and-parallelism.ipynb) for the reasoning behind each of these.

## Picking the engine

| Work is… | Use | Why |
| --- | --- | --- |
| waiting on I/O (network, disk, DB) | `ThreadPoolExecutor` | threads release the GIL while waiting |
| computing (parse, hash, crunch) | `ProcessPoolExecutor` | separate interpreters dodge the GIL |
| thousands of async-capable I/O calls | neither — use [`asyncio`](asyncio-cheatsheet.md) | scales further on one thread |
