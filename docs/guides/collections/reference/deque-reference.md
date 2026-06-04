---
title: deque reference
---

# `deque` reference

A double-ended queue: a sequence with fast appends and pops at *both* ends.

```python
from collections import deque
```

## Construction

| Form | Result |
| --- | --- |
| `deque()` | empty |
| `deque(iterable)` | filled from an iterable |
| `deque(iterable, maxlen=N)` | bounded — never holds more than `N` items |

With a `maxlen`, appending to a full deque drops an item from the **opposite** end. `d.maxlen` reports the limit (`None` if unbounded).

## Methods

| Method | Does | Cost |
| --- | --- | --- |
| `append(x)` | add on the right | O(1) |
| `appendleft(x)` | add on the left | O(1) |
| `pop()` | remove & return from the right | O(1) |
| `popleft()` | remove & return from the left | O(1) |
| `extend(iterable)` | append many on the right | O(k) |
| `extendleft(iterable)` | append many on the left — **reverses order** | O(k) |
| `rotate(n)` | shift `n` steps right (negative = left) | O(k) |
| `remove(value)` | delete first matching value | O(n) |
| `insert(i, x)` | insert at index `i` | O(n) |
| `index(x)` / `count(x)` | search | O(n) |
| `reverse()` / `clear()` | in place | O(n) / O(1) |
| `d[i]` | index access | O(1) at ends, O(n) in the middle |

`len(d)`, iteration, `in`, and slicing-by-index all work as on a list (though random middle access is slower).

## Complexity: `deque` versus `list`

| Operation | `list` | `deque` |
| --- | --- | --- |
| append / pop at the **end** | O(1) | O(1) |
| append / pop at the **front** | **O(n)** | **O(1)** |
| index in the middle (`x[i]`) | O(1) | O(n) |
| insert/delete in the middle | O(n) | O(n) |

So: a `list` wins for random access by index; a `deque` wins decisively for work at the front (queues, buffers).

## When to use a `deque`

| Need | Pattern |
| --- | --- |
| FIFO queue | `append` to add, `popleft` to serve |
| stack (LIFO) | `append` / `pop` (a `list` is equally fine) |
| last N items / sliding window | `deque(maxlen=N)` |
| ring buffer | `deque(maxlen=N)` |
| cycling through items | `rotate` |

For heavy random indexing or middle insertion, prefer a `list`; for two-ended work, prefer a `deque`.
