---
title: Generator syntax reference
---

# Generator syntax reference

Everything generator-specific: `yield`, `yield from`, `.send()`, `.close()`, `.throw()`, generator expressions.

## Generator functions

Any function with `yield` anywhere in its body becomes a generator function. Calling it doesn't run the body — it returns a generator object (an iterator).

```python
def counter(start, stop):
    while start < stop:
        yield start
        start += 1
```

Key behaviours:

- Function body pauses at each `yield`, resumes on next `next()`.
- Local variables are preserved across pauses.
- Falling off the end is equivalent to a bare `return` — raises `StopIteration`.

## `yield` as a statement

```python
def g():
    yield                  # yield None
    yield 42               # yield a value
    yield 1, 2, 3          # yield a tuple
```

All three are statements. The parentheses-less form `yield 1, 2, 3` yields a *tuple*, not three separate values.

## `yield` as an expression

Inside a generator, `yield` is also an expression. Its value is whatever was sent in via `.send()` on the generator object (or `None` for plain `next()` calls).

```python
def echo():
    received = yield 'start'
    while True:
        received = yield f'got: {received}'

g = echo()
print(next(g))             # 'start'
print(g.send('hello'))     # 'got: hello'
print(g.send('world'))     # 'got: world'
```

This is the basis for generator-based coroutines. In modern code, `async def`/`await` is usually the better choice, but the mechanism still exists.

## `yield from` — delegation

```python
def inner():
    yield 1
    yield 2

def outer():
    yield 'a'
    yield from inner()     # yields each value from inner
    yield 'b'
```

What `yield from` does:

| Feature | Behaviour |
| --- | --- |
| Iteration | Yields every value from the sub-iterable. |
| `send` | Values sent to the outer generator are forwarded to the inner generator. |
| Exceptions | `.throw()` on the outer is forwarded to the inner. |
| Return value | The value attached to the inner generator's `StopIteration` becomes the *value* of the `yield from` expression. |

```python
def inner():
    yield 1
    yield 2
    return 'done'

def outer():
    result = yield from inner()
    print(f'inner returned: {result}')    # 'done'
    yield 3

print(list(outer()))
```

Without `yield from`, you'd write `for x in inner(): yield x` — which works for simple iteration but not for send/throw delegation.

## Generator methods

Every generator object exposes these methods.

### `.send(value)`

Resumes the generator. The `yield` expression inside the generator evaluates to `value`. Returns the next yielded value (or raises `StopIteration`).

```python
g = echo()
next(g)                    # advance to first yield
g.send('hello')
```

Note: you cannot call `.send(value)` on a fresh generator — call `next(g)` first (or `g.send(None)`) to advance it to the first yield.

### `.close()`

Injects `GeneratorExit` at the current `yield`. The generator can catch it in a `finally` block for cleanup, but should not yield again (doing so raises `RuntimeError`).

```python
def with_cleanup():
    try:
        while True:
            yield input()
    finally:
        print('cleaning up')

g = with_cleanup()
g.close()                  # prints 'cleaning up'
```

### `.throw(exc)`

Raises an exception at the current `yield`. The generator can catch it or let it propagate.

```python
def resilient():
    while True:
        try:
            yield
        except ValueError as e:
            print(f'caught {e}; continuing')

g = resilient()
next(g)
g.throw(ValueError('oops'))
```

## Generator expressions

```python
squares = (x * x for x in range(10))
```

Same syntax as list comprehensions, but with round brackets. Evaluates lazily; returns a generator object; one-shot.

### Parentheses can be omitted when a genexp is a function's sole argument

```python
sum(x * x for x in range(10))        # fine
max(len(w) for w in words)           # fine

some_func(x * x for x in xs, extra)  # NOT fine — needs explicit parens around the genexp
```

### Multiple clauses

```python
((a, b) for a in range(3) for b in range(3) if a != b)
```

Multiple `for` clauses are read left-to-right, same as nested loops.

### Genexps use a new scope

The loop variable doesn't leak into the enclosing scope:

```python
g = (i for i in range(5))
try:
    print(i)              # NameError
except NameError as e:
    print(e)
```

Whereas list comprehensions also scope their variable (Python 3) — this part is consistent.

## `@generator` vs async generators

Python supports async generators (`async def` + `yield`):

```python
async def stream():
    yield 1
    yield 2
```

These are driven by `async for` and `await` rather than plain `next()`. They're a different beast from regular generators and belong in the async guide. Don't mix the two.

## Quick table — generator vs. list

| Attribute | List comprehension | Generator expression |
| --- | --- | --- |
| Syntax | `[expr for x in it]` | `(expr for x in it)` |
| Eagerness | Materialises immediately | Lazy — on demand |
| Memory | O(n) | O(1) overhead |
| Re-iterable | Yes | No (one-shot) |
| Indexable | Yes | No |
| Right choice for… | Iterating multiple times, indexing, debugging | Single-pass, large/infinite, pipelines |

## Related references

- [Iterator protocol reference](iterator-protocol-reference.md) — the `__iter__`/`__next__` contract generators implement.
- [`itertools` cheatsheet](itertools-cheatsheet.md) — ready-made generators from the standard library.
