---
title: asyncio cheatsheet
---

# `asyncio` cheatsheet

The everyday `asyncio` surface on one page. Coroutines do nothing until awaited or scheduled; the event loop runs whichever scheduled task is ready.

```python
import asyncio
```

## Entry point

| Call | Does | Notes |
| --- | --- | --- |
| `asyncio.run(coro)` | start a loop, run `coro` to completion, close the loop | the one bridge from sync to async; call **once**, at the top |
| `await coro` | run `coro`, get its result | only valid inside an `async def` |

`asyncio.run` raises `RuntimeError` if a loop is already running (e.g. in a notebook — `await` directly there).

## Running things concurrently

| Call | Yields | Notes |
| --- | --- | --- |
| `await asyncio.gather(*coros)` | list of results, in order | re-raises first exception unless `return_exceptions=True` |
| `await asyncio.gather(*coros, return_exceptions=True)` | results and exceptions as values | nothing raised; sort them yourself |
| `task = asyncio.create_task(coro)` | a `Task` (runs in background) | starts at the next `await`; `await task` for its result |
| `async with asyncio.TaskGroup() as tg:` then `tg.create_task(coro)` | structured batch (3.11+) | block exits when all finish; one failure cancels the rest |

```python
async with asyncio.TaskGroup() as tg:          # 3.11+, preferred
    t1 = tg.create_task(fetch('a'))
    t2 = tg.create_task(fetch('b'))
print(t1.result(), t2.result())
```

## Waiting and time

| Call | Does |
| --- | --- |
| `await asyncio.sleep(seconds)` | non-blocking sleep — yields to the loop (never `time.sleep`) |
| `await asyncio.sleep(0)` | yield once, letting other tasks run |
| `async with asyncio.timeout(s): ...` | cancel the block after `s`, raise `TimeoutError` (3.11+) |
| `await asyncio.wait_for(coro, timeout=s)` | run `coro` with a deadline; raise `TimeoutError` (all versions) |
| `done, pending = await asyncio.wait(tasks, return_when=...)` | wait on a set; `FIRST_COMPLETED`, `FIRST_EXCEPTION`, `ALL_COMPLETED` |
| `for c in asyncio.as_completed(coros): r = await c` | iterate results as they finish |

## Offloading blocking / CPU work

| Call | Use for | Runs on |
| --- | --- | --- |
| `await asyncio.to_thread(fn, *args)` | a blocking **I/O** call you can't change | a worker thread |
| `await loop.run_in_executor(pool, fn, *args)` | CPU-bound work (`pool=ProcessPoolExecutor`) or custom pools | that executor |
| `loop = asyncio.get_running_loop()` | get the loop (inside a coroutine) | — |

Never run a long synchronous call directly in a coroutine — it freezes every task until it returns.

## Synchronisation primitives

All are `async`-aware: acquire with `async with`, await where noted. Use them to coordinate tasks, **not** to protect against threads.

| Primitive | Purpose | Typical use |
| --- | --- | --- |
| `asyncio.Lock()` | mutual exclusion between tasks | `async with lock:` around a critical section |
| `asyncio.Semaphore(n)` | allow at most `n` tasks at once | `async with sem:` to bound fan-out |
| `asyncio.Event()` | one-to-many signal | `await event.wait()` / `event.set()` |
| `asyncio.Condition()` | wait for a condition with a lock | producer/consumer coordination |
| `asyncio.Queue(maxsize=0)` | hand work between tasks | `await q.put(x)` / `x = await q.get()`; `q.task_done()`, `await q.join()` |

## Cancellation

| Call | Does |
| --- | --- |
| `task.cancel()` | request cancellation; raises `CancelledError` inside the task at its next `await` |
| `task.cancelled()` / `task.done()` | inspect state |
| `try: ... except asyncio.CancelledError: ...` | clean up on cancel — then **re-raise**, don't swallow it |

A `TaskGroup` cancels its siblings automatically when one task errors, which is why it's preferred over manual `gather` + cancellation.

## Quick decision

- A handful of awaitables, want all results → `gather`.
- A batch with proper error handling (3.11+) → `TaskGroup`.
- Start something now, collect later → `create_task`.
- Cap how many run at once → `Semaphore`.
- Calling blocking code → `asyncio.to_thread` (I/O) or `run_in_executor` with a process pool (CPU).
