---
title: threading and multiprocessing reference
---

# Threading and multiprocessing reference

The lower-level primitives behind the [`concurrent.futures`](concurrent-futures-reference.md) pools. Reach for these when a pool isn't the right shape — long-lived workers, producer/consumer pipelines, or fine-grained synchronisation. For most "run this over many inputs" jobs, prefer the executors.

## `threading`

```python
import threading
```

### Creating and running threads

| Call | Does |
| --- | --- |
| `t = threading.Thread(target=fn, args=(...), kwargs={...})` | create a thread to run `fn` |
| `t.start()` | run it on a new thread |
| `t.join(timeout=None)` | block until it finishes |
| `t.daemon = True` (before start) | thread won't keep the program alive |
| `threading.current_thread()` / `threading.get_ident()` | identify the running thread |

Threads share memory and run Python one at a time (the GIL). Good for I/O-bound work, useless for CPU-bound.

### Synchronisation

| Primitive | Purpose |
| --- | --- |
| `Lock()` | mutual exclusion; `with lock:` around a critical section. Acquiring twice in one thread deadlocks. |
| `RLock()` | reentrant lock — the same thread may acquire it repeatedly |
| `Event()` | a flag threads can `wait()` on and `set()`/`clear()` |
| `Condition()` | `wait()`/`notify()` on a shared predicate, with an internal lock |
| `Semaphore(n)` | allow at most `n` holders at once |
| `Barrier(n)` | release all parties once `n` are waiting |

```python
lock = threading.Lock()
with lock:                 # only one thread inside at a time
    shared += 1
```

### `queue.Queue` — the thread-safe handoff

```python
import queue
q = queue.Queue(maxsize=0)        # 0 = unbounded
q.put(item)                       # blocks if full
item = q.get()                    # blocks if empty
q.task_done()                     # mark one item processed
q.join()                          # block until every put item is done
```

`queue.Queue` is the idiomatic, lock-free way to pass work between threads — prefer it over manually locking a shared list.

## `multiprocessing`

```python
import multiprocessing as mp
```

Each process is a separate interpreter with its own memory and GIL — true parallelism for CPU-bound work. Launch under `if __name__ == "__main__":`.

### Processes and pools

| Call | Does |
| --- | --- |
| `p = mp.Process(target=fn, args=(...))` | a process (same API shape as `Thread`) |
| `p.start()` / `p.join()` | run it / wait for it |
| `with mp.Pool(processes=None) as pool:` | a worker pool (older sibling of `ProcessPoolExecutor`) |
| `pool.map(fn, iterable, chunksize=...)` | parallel map, results in order |
| `pool.apply_async(fn, args)` | submit one, returns an `AsyncResult` (`.get()` for the value) |

For new code, `concurrent.futures.ProcessPoolExecutor` is the friendlier interface; use `mp.Pool` when you need its specific methods.

### Start methods

| Method | Default on | Behaviour |
| --- | --- | --- |
| `spawn` | Windows, macOS | fresh interpreter, imports your module (hence the `__main__` guard) |
| `fork` | Linux | copies the parent process; faster but can inherit unwanted state |
| `forkserver` | (opt-in) | a clean server process forks workers |

Set it explicitly with `mp.set_start_method("spawn")` for cross-platform consistency.

### Sharing data between processes

Processes don't share memory, so prefer **returning** results over sharing state. When you genuinely need shared state:

| Tool | Use |
| --- | --- |
| `mp.Queue()` / `mp.Pipe()` | pass messages between processes |
| `mp.Value(typecode, init)` | a single shared scalar (e.g. `mp.Value('i', 0)`) |
| `mp.Array(typecode, size)` | a shared fixed-size array |
| `with mp.Manager() as m:` | server-backed shared `list`, `dict`, etc. (slower, flexible) |
| `mp.Lock()` / `mp.Semaphore()` | synchronise access to shared objects |

```python
counter = mp.Value('i', 0)
with counter.get_lock():           # shared updates still need locking
    counter.value += 1
```

Everything crossing a process boundary must be **picklable**.

## Which to use

| Situation | Reach for |
| --- | --- |
| run a function over many inputs | a `concurrent.futures` pool, not these |
| I/O-bound, a few long-lived workers + a work queue | `threading.Thread` + `queue.Queue` |
| CPU-bound, custom orchestration | `multiprocessing.Process` / `Pool` |
| coordinating tasks (signal, gate, limit) | the matching `Lock`/`Event`/`Semaphore` |
