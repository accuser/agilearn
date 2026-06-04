# Avoid common concurrency mistakes

**The question.** Something is wrong with concurrent code — a counter ends up too low, a program spawns endlessly on start, an async batch runs no faster than sequential, a task fails silently. You want the short list of traps and the fix for each.

Most of these trace back to three facts: threads share memory (so updates collide), processes don't (so data must be pickled and code guarded), and async runs on one thread (so anything that doesn't yield freezes everything).

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| Counter ends up lower than expected | race: `x += 1` is read-modify-write, threads interleave | guard with a `Lock`, or return values and combine in the parent |
| Program spawns processes forever / errors on start | child re-imports the script and re-runs pool creation | wrap launch in `if __name__ == "__main__":` |
| Async batch no faster than sequential | a blocking call (`time.sleep`, `requests`) never yields | use async equivalents; offload blocking work with `asyncio.to_thread` |
| `RuntimeWarning: coroutine was never awaited` | you called an `async def` but didn't await it | `await coro`, or schedule with `create_task` / `gather` |
| Threads give no speedup on computation | the GIL serialises Python bytecode | use `ProcessPoolExecutor` for CPU-bound work |
| A task failed but nothing was reported | exception is stored on the `Future`, not raised | call `future.result()` (or check `future.exception()`) |
| Program hangs forever | deadlock — same lock acquired twice, or lock-order cycle | use `RLock` for re-entry; always acquire locks in a fixed order |
| `PicklingError` on a lambda/local function | process workers receive the function via `pickle` | define the worker at module top level |
| `gather` aborts the whole batch on one error | default re-raises the first exception | pass `return_exceptions=True` and sort results |
| Sockets exhausted / rate-limited | unbounded fan-out — everything launched at once | bound with `asyncio.Semaphore(n)` or a pool's `max_workers` |
| `asyncio.run()` raises "loop is already running" | called from inside a running loop (e.g. a notebook) | `await main()` there; use `asyncio.run` only at a script's top |
| Shared list/dict corrupts across threads | concurrent mutation without synchronisation | lock the section, or give each task its own and merge after |

Each in turn below.

## Why each one bites

### 1. Races on shared mutable state

`counter += 1` compiles to read the value, add one, write it back. Two threads can both read the same old value, both add one, and both write — one increment is lost. Anything that isn't a single atomic operation needs protection:

```python
lock = threading.Lock()
with lock:
    counter += 1          # only one thread in here at a time
```

Better still, avoid the shared variable: have each task `return` its contribution and sum the returns in the main thread, where there's no concurrency at all.

### 2. The missing `__main__` guard

`ProcessPoolExecutor` and `multiprocessing` create workers by starting a new interpreter that **imports your module**. If the code that creates the pool runs at import time, every child runs it too, each spawning more children. The guard confines launch to the original process:

```python
def main():
    with ProcessPoolExecutor() as pool:
        ...

if __name__ == "__main__":
    main()
```

### 3. Blocking the event loop

Async concurrency works only because tasks yield at `await`. A synchronous call that takes time — `time.sleep(5)`, `requests.get(...)`, a synchronous DB driver, a CPU-heavy loop — doesn't yield, so the loop and every other task freeze until it returns. Use async-native libraries, or push the blocking call to a thread:

```python
result = await asyncio.to_thread(blocking_function, arg)   # runs off the loop
```

### 4. Coroutines that are never awaited

Calling an `async def` returns a coroutine object and runs *nothing*. Forgetting the `await` (or a `create_task`) means the work silently doesn't happen, and Python warns `coroutine was never awaited`:

```python
fetch(url)              # WRONG: nothing runs
await fetch(url)        # runs it
task = asyncio.create_task(fetch(url))   # schedules it to run concurrently
```

### 5. Threads for CPU-bound work

The GIL allows only one thread to execute Python bytecode at a time, so threads give no parallel speedup for pure computation — they just add overhead. Computation needs separate interpreters:

```python
with ProcessPoolExecutor() as pool:     # not ThreadPoolExecutor
    results = list(pool.map(cpu_heavy, items))
```

### 6. Swallowed exceptions

An exception in a pool worker doesn't crash the program — it's stored on the `Future` and only surfaces when you call `.result()`. Fire-and-forget tasks therefore hide their failures:

```python
for future in as_completed(futures):
    try:
        use(future.result())            # re-raises here if the task failed
    except Exception as exc:
        log(exc)
```

### 7. Deadlocks

Two ways to hang: acquire a non-reentrant `Lock` you already hold (use `RLock` if a thread must re-enter), or have two threads each hold one lock and wait for the other's. The cure for the second is discipline — always acquire multiple locks in the same global order everywhere.

### 8. Un-picklable arguments to processes

Process workers receive their function and arguments via `pickle`. Lambdas, locally defined functions, open files, sockets, and locks can't be pickled. Move the worker to module top level and pass plain data:

```python
def worker(x):          # top level, picklable
    return x * x
```

### 9. `gather` aborting on the first failure

By default `asyncio.gather` re-raises the first exception and you lose the other results. To complete the whole batch and inspect failures, return them as values:

```python
outcomes = await asyncio.gather(*tasks, return_exceptions=True)
errors = [o for o in outcomes if isinstance(o, Exception)]
```

### 10. Unbounded fan-out

Launching thousands of tasks at once exhausts file descriptors, sockets, or a remote service's rate limit. Cap concurrency:

```python
sem = asyncio.Semaphore(20)
async with sem:                # at most 20 in flight
    await do_work()
```

For thread/process pools, the equivalent knob is `max_workers`.

### 11. `asyncio.run` inside a running loop

`asyncio.run` creates and owns a fresh event loop, so calling it where one is already running — inside a notebook, or nested in another coroutine — raises `RuntimeError`. Use `asyncio.run(main())` once at a script's entry point; everywhere inside async code, `await` directly.

### 12. Concurrent mutation of shared collections

Lists and dicts aren't safe to mutate from multiple threads simultaneously; you can lose writes or corrupt internal state. Either lock every access, or — far simpler — hand each thread its own structure and merge the results once they've all joined.

## The meta-lesson

Almost every fix above is a variant of one principle: **share as little mutable state as possible.** Tasks that take inputs and return outputs, with the combining done in one place, sidestep races, locks, deadlocks, and most pickling problems at a stroke. Reach for locks and shared memory only when the algorithm genuinely demands it.
