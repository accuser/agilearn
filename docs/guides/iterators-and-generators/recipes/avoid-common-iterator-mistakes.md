# Avoid common iterator mistakes

**The question.** Something odd is happening with a generator or iterator — an empty result from a `sum` that worked moments ago, a `for` loop that skips elements, a pipeline that silently does nothing. You want the short list of traps and the fix for each.

Most of these are consequences of two facts: iterators are *consumed once*, and generators only do work when you *pull* values.

## The answer

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `sum(it); sum(it)` returns `0` the second time | iterator already exhausted | keep the iterable, or re-call the generator function |
| `items.remove(x)` inside `for x in items` | index shifts under the loop | build a new list, or iterate `list(items)` |
| `return value` in a generator | becomes `StopIteration.value`; `for` discards it | write a regular function if you want a return value |
| `[(i + x for x in r) for i in range(3)]` all identical | late binding of `i` | bind early with a helper function or default argument |
| `iter(some_function)` raises `TypeError` | functions aren't iterable | use `iter(callable, sentinel)` |
| `next(it)` raises `StopIteration` in your code | one-arg form has no default | use `next(it, default)` |
| `max(gen)` raises on empty generator | no default | pass `default=...` |
| pipeline never runs | nothing consumes it | `list(...)`, `for _ in ...`, or a reducer |
| `sorted(huge_gen)` uses all memory | `sorted` is eager | `heapq.nlargest(k, ...)` for top-k |
| groupby sub-iterator is empty after outer loop advances | they expire | materialise `list(group)` inside the loop |

Each in turn below.

## Why each one bites

### 1. Iterating an iterator twice

```python
it = iter([1, 2, 3])
first  = sum(it)         # 6
second = sum(it)         # 0  — already exhausted
```

The second `sum` returns the empty-sum value without raising. Keep the *iterable* and call `iter()` again, or materialise into a list. If your 'iterable' is really a generator function, re-call the function each time.

### 2. Mutating a list while iterating it

```python
items = [1, 2, 3, 4, 5]
for x in items:
    if x % 2:
        items.remove(x)        # '3' survives!
```

The iterator holds an index internally; removing shifts elements out from under the loop. `dict` and `set` raise `RuntimeError: dictionary changed size during iteration` instead of silently misbehaving. Fix: build a new list, or iterate a copy.

### 3. `return value` inside a generator

A `return` from a generator stops iteration; a `return value` attaches `value` to the `StopIteration` exception, which `for` loops discard. If you want to *return* something, write a regular function — not a generator.

### 4. Late binding in generator expressions

```python
gens = [(i + x for x in range(2)) for i in range(3)]
for g in gens:
    print(list(g))    # [2, 3], [2, 3], [2, 3] — all see final i
```

Each generator sees the *current* value of `i` at consumption time, not the value when it was created. Fix: capture via a helper function or a default argument so binding happens per call.

### 5. `iter()` on a callable

`iter(fn)` raises `TypeError` — functions aren't iterable. The two-argument form `iter(fn, sentinel)` calls `fn()` repeatedly until it returns the sentinel. Handy for 'read until empty' loops.

### 6. `next(it)` instead of `next(it, default)`

Single-argument `next` raises `StopIteration` on exhaustion. Inside a `for` loop that's fine. Leaking `StopIteration` out of your own code is confusing, and inside a generator it triggers PEP 479 errors. Pass a default unless you specifically want the exception.

### 7. `min`/`max`/`sum` on empty input

`min` and `max` raise `ValueError`; `sum` quietly returns `0`. Pass a `default=` argument when the stream might be empty.

### 8. Forgetting to consume

```python
def shouts(xs):
    for x in xs:
        print(f'shouting {x}')
        yield x.upper()

shouts(['hi', 'there'])     # nothing happens
```

A pipeline does no work until something drives it. Wrap in `list(...)`, iterate with `for`, or pass to a reducer. No consumer, no output.

### 9. `sorted(huge_iterable)` eats memory

`sorted` has to see every element before it can return one. For huge streams that kills the constant-memory property of the rest of your pipeline. If you only need top-*k*, `heapq.nlargest(k, iterable)` is O(n) time and O(k) memory.

### 10. `groupby` sub-iterators expire

```python
saved = [(k, g) for k, g in groupby(items, key=...)]
for k, g in saved:
    print(list(g))     # all empty
```

Sub-iterators are only valid while the outer loop is on that iteration. Materialise `list(group)` inside the loop if you need to use it later.

### 11. `filter` vs. `takewhile`/`dropwhile`

`filter(pred, it)` scans the whole stream; `takewhile(pred, it)` stops at the first non-match. If you want 'keep until I see X', reach for `takewhile` — don't use `filter` and break out manually.

## When it isn't a bug

Several of these are patterns, not absolute rules. Exhausting an iterator deliberately (to 'consume the rest') is fine. Late binding is sometimes what you want — a generator that reacts to the current state of a shared variable. Building a `list(...)` of a stream is fine when the stream comfortably fits in memory.

The traps bite when the shortcut is applied reflexively to a case where the defaults don't match the intent. If you're seeing a bug from this list, the fix is almost always small; if the shortcut is correct, move on.

## Related reading

- [Chain and group iterables](chain-and-group-iterables.ipynb) — the correct shape for `groupby` and `zip`.
- [Combine generators into a pipeline](combine-generators.ipynb) — the forgotten-consumer trap in context.
- [Process a large file lazily](process-a-large-file-lazily.ipynb) — the `readlines` anti-pattern and its fixes.
- [itertools cheatsheet](../reference/itertools-cheatsheet.md) — including `takewhile`, `dropwhile`, `chain`, `groupby`.
